#include <iostream>
#include <thread>
#include <mutex>
#include <vector>
#include <map>
#include <chrono>


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
        ++shared->array[shared->counter];
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
    int array_size{1000000};
    int cycles{5};

    vector<void(*)(Shared*)> counter_functions(0);
    counter_functions.push_back(counter1);
    counter_functions.push_back(counter2);
    counter_functions.push_back(counter3);

    for(auto& cntr : counter_functions) {
        int sum = 0;
        for(int i = 0; i < cycles; ++i) {
            Shared s(array_size);
            auto start = chrono::high_resolution_clock::now();

            thread t1(cntr, &s);
            thread t2(cntr, &s);
            t1.join();
            t2.join();

            auto end = chrono::high_resolution_clock::now();
            sum += chrono::duration_cast<chrono::milliseconds>(end - start).count();

            print_histogram(s.array);
        }
        cout << "Average duration [ms]: " << static_cast<int>(sum / cycles) << endl;
    }

    return 0;
}
