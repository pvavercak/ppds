#include <iostream>
#include <thread>
#include <mutex>
#include <vector>
#include <map>
#include <chrono>
#include <fstream>


using namespace std;


class Shared {
public:
    int counter{0};
    int end{0};
    vector<int> array;
    mutex mtx{};

    Shared() = delete;
    Shared(int end) : end(end) {
        array = vector<int>(end, 0);
    }
};


void counter1(Shared *shared) {
    while (1) {
        if (shared->counter >= shared->end)
            break;
        shared->mtx.lock();
        if (shared->counter < shared->end) {
            ++shared->array[shared->counter];
        }
        ++shared->counter;
        shared->mtx.unlock();
    }
}


void counter2(Shared *shared) {
    while (1) {
        shared->mtx.lock();
        if (shared->counter >= shared->end) {
            shared->mtx.unlock();
            break;
        }
        ++shared->array[shared->counter];
        ++shared->counter;
        shared->mtx.unlock();
    }
}


void counter3(Shared *shared) {
    while (1) {
        shared->mtx.lock();
        int cnt = shared->counter;
        ++shared->counter;
        shared->mtx.unlock();
        if (cnt >= shared->end)
            break;
        ++shared->array[cnt];
    }
}


template<typename T>
void print_histogram(const vector<T> &array) {
    map<T, int> histogram;
    for(const auto& elem : array) {
        if (histogram.find(elem) != histogram.end()) {
            ++histogram[elem];
        } else {
            histogram[elem] = 1;
        }
    }

    for(const auto& elem : histogram) {
        cout << elem.first << ": " << elem.second << "x, ";
    }
    cout << endl;
}


int main(int argc, char** argv) {
    ofstream out_csv{"report.csv"};

    if (!out_csv) {
        std::cout << "Problem opening output file" << endl;
        return EXIT_FAILURE;
    }

    out_csv << "threads;time_counter1;time_counter2;time_counter3" << endl;

    int array_size{10000000};
    int cycles{10};

    vector<void(*)(Shared*)> counter_functions({
        counter1, counter2, counter3});

    for(int thread_count = 1; thread_count <= 128; thread_count*=2) {
        out_csv << thread_count << ";";
        for(int fnc = 0; fnc < counter_functions.size(); ++fnc) {
            int sum_of_times = 0;
            for(int i = 0; i < cycles; ++i) {
                Shared s(array_size);
                vector<thread> threads;
                auto start = chrono::high_resolution_clock::now();

                for(int th = 0; th < thread_count; ++th) {
                    threads.push_back(thread(counter_functions[fnc], &s));
                }

                for(thread& th : threads) {
                    if (th.joinable()) {
                        th.join();
                    }
                }

                auto end = chrono::high_resolution_clock::now();

                sum_of_times += 
                    chrono::duration_cast<chrono::milliseconds>(
                        end - start
                    ).count();
            }
            out_csv << static_cast<int>(sum_of_times / cycles);
            if (fnc != counter_functions.size() - 1) {
                out_csv << ";";
            }
        }
        out_csv << endl;
    }

    out_csv.close();

    return EXIT_SUCCESS;
}
