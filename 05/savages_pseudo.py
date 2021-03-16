
def init():
    N_SAVAGES  # nejaky pocet divochov > 0
    N_COOKS  # nejaky pocet kucharov > 0

    # jednoduchy mutex
    mutex = Mutex()

    # synch. obj. typu bariera pre divochov
    barrier1 = SimpleBarrier(N_SAVAGES)
    barrier2 = SimpleBarrier(N_SAVAGES)

    # synch. obj. typu bariera pre kucharov
    cookBarrier1 = SimpleBarrier(N_COOKS)
    cookBarrier2 = SimpleBarrier(N_COOKS)

    # na zaciatku je nenavarene, hned potom, co su kuchari zobudeni,
    # navaria plny hrniec, co je simulovane priradenim N_SAVAGES do tejto premennej
    servings = 0

    # semafor, ktory pouzijeme na signalizaciu kucharom, aby varili
    empty_pot = Semaphore(0)

    # semafor, ktory pouzijeme na signalizaciu divochom, ze uz je navarene
    full_pot = Semaphore(0)

    # lightswitch, ktory budu stale prepinat ti kuchari,
    # ktori ako posledni dovarili alebo ako prvi boli zobudeni
    lightswitch = LightSwitch

    # pustime vlakna
    for cook_id in range(N_COOKS):
        create_and_run_thread(cook, cook_id)
    for savage_id in range(N_SAVAGES):
        create_and_run_thread(savage, savage_id)


def savage(savage_id):
    while True:
        # dvojita bariera zabezpeci, aby sa divosi nepredbiehali
        # a aby vsetci dostali rovnakym dielom
        barrier1.wait()
        barrier2.wait()
        # vzajomne vylucenie, ideme do KO
        mutex.lock()
        # kontrola, ci mame 0 porcii a treba budit kucharov
        if not servings:
            # kontrolny vypis, aby sme vedeli, ze len jeden zobudi kucharov
            print(f"divoch {savage_id}: budim kuchara")
            # signalizujeme prazdny hrniec
            # na tomto semafore caka prvy z kucharov
            empty_pot.signal()
            # po signalizovani kucharovi si divoch pocka na dodanie porcii
            full_pot.wait()
        # hrniec je naplneny, divosi ale nemozu brat porcie naraz,
        # lebo sme neodomkli mutex
        get_serving()
        # odomkneme mutex, divosi mozu paralelne jest
        mutex.unlock()
        # simulujeme jedenie
        eat_serving()


def cook(cook_id):
    while True:
        # zabezpecim pomocou lightswitchu, ze iba jediny kuchar caka na prazdny hrniec
        lightswitch.lock()
        # simulujeme varenie jedla
        make_servings()
        # pockame, ked vsetci kuchari dorobia svoj diel
        cookBarrier1.wait()
        # zabezpecim pomocou lightswitch ADT, ze posledny kuchar zavola signal() nad full_pot
        # este pred zhasnutim lightswitchu sa do servings priradi novy pocet porcii
        lightswitch.unlock()
        # pockam, kym vsetci prejdu lightswitchom,
        # aby nejake vlakno neprebehlo na zaciatok cyklu
        cookBarrier2.wait()
