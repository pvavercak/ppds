"""
V nasom modeli simulujeme prevadzku kadernictva,
ktore ma kapacitu CAP a takisto ma stalu klientelu N_CUSTOMERS,
to znamena, ze do kadernictva sa nahodne chodi strihat ten isty
pocet zakaznikov potom, co im narastu vlasy.
Zakaznici sa spravaju podla toho, ako je naplnene kadernictvo.
Ak pride zakaznik a vidi, ze kadernictvo nema prekrocenu kapacitu,
posadi sa do cakacieho kresla a signalizuje kadernikovi,
ze mu prisiel zakaznik. Nasledne pocka, kym sa barber uvolni a kedze vyuzivame
FIFO (silny) semafor, tak vieme, ze prvy zakaznik, ktory vyvolal wait()
nad barber semaforom, sa dostane na rad akonahle barber skonci s aktualne
strihanym zakaznikom.
Ak je kadernictvo plne, tak zakaznik pride inokedy, teda caka v nahodnom intervale,
kym sa pokusi o strih v kadernictve.
"""

def init():
    # definujeme kapacitu kadernictva, teda pocet kresiel (vratane hlavneho) je CAP
    CAP = 2
    # pocet zakaznikov, ktori su stalymi zakaznikmi kadernictva
    N_CUSTOMERS = 6
    # objekt Shared, ktory uchovava pocet zakaznikov aktualne v kadernictve a takisto aj kapacitu kadernictva
    shared = Shared(cap)
    mutex = Mutex()

    barber = Semaphore(0)
    customer = Semaphore(0)

    barber_done = Semaphore(0)
    customer_done = Semaphore(0)


def create_and_run_threads():
    threads = []
    # N_CUSTOMERS vlakien pre cinnost zakaznikov
    for _ in range(N_CUSTOMERS):
        threads.append(Thread(customer, shared))

    # jedno vlakno pre barbera
    threads.append(Thread(barber, shared))


def customer(shared):
    while True:
        # zachovame integritu, takze pred kontrolou kapacity zamkneme mutex
        shared.mutex.lock()
        # ak je kapacita prekrocena
        if shared.N == shared.customers:
            # zakaznik odomkne mutex
            shared.mutex.unlock()
            # ide cakat, skusi to opat znovu po nejakom case
            try_next_time()
        # pripad, ked v kadernictve nie je plno a zakaznik sa dostane k volnemu kreslu
        else:
            # zakaznik prisiel, zvysi pocet vsetkych zakaznikov v kadernictve
            shared.customers += 1
            # odomkneme mutex v else vetve
            shared.mutex.unlock()
            # zakaznik signalizuje kadernikovi, ze sa prisiel ostrihat
            shared.customer.signal()
            # zakaznik pocka na kadernika, kym skonci s aktualne strihanym zakaznikom
            shared.barber.wait()
            
            # zakaznik sa dostal na rad, striha sa
            get_haircut()

            # zakaznik je spokojny s ucesom, povie barberovi, ze je hotovo
            shared.customer_done.signal()
            # pocka, kym barber dokonci posledne upravy
            shared.barber_done.wait()

            # zakaznik odchadza, znizuje pocet zakaznikov v kadernictve
            # musime zachovat integritu premennej customers v shared objekte, preto mutex
            shared.mutex.lock()
            shared.customers -= 1
            shared.mutex.unlock()

            # zakaznik caka, kym mu znovu nenarastu vlasy, potom sa moze prist ostrihat znova
            grow_hair()


def barber(shared):
    while True:
        # kadernik caka, kym mu nejaky zakaznik neda signal, ze prisiel po novy strih
        shared.customer.wait()
        # barber signalizuje zakaznikovi, ze ho berie
        shared.barber.signal()

        # barber ostriha zakaznika
        cut_hair(shared.customers - 1)

        # barber upravuje zakaznikovi vlasy az kym zakaznik nesignalizuje, ze je spokojny s novym ucesom
        shared.customer_done.wait()
        # barber signalizuje, ze dokoncil svoju pracu, obdrzal poplatok za strihanie, moze strihat dalsieho zakaznika
        shared.barber_done.signal()
