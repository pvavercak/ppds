
def init():
    # objekt pre signalizaciu zapisu do uloziska
    valid_data = Event()
    # semafor pre monitor, aby zablokoval cidla
    block_sensors = Semaphore(1)
    # semafor pre cidlo, aby zablokovalo monitory
    block_monitors = Semaphore(1)
    # LightSwitch, pre kazdu kategoriu vlastny
    sensor_ls = LightSwitch()
    monitor_ls = LightSwitch()

    for monitor_id in <0, 7>:
        create_and_run_thread(monitor, monitor_id)
    for sensor_id in <0, 2> :
        create_and_run_thread(monitor, sensor_id)


def monitor(monitor_id):
    # pockame, kym cidlo signalizuje udalost zapisania do uloziska
    valid_data.wait()
    while True:
        # zabezpecime blokovanie cidiel,
        # takze uz 1. cidlo sa nepohne zo sensor_ls.lock()
        block_monitors.wait()
        
        # Vylucime vlakna vykonavajuce funkciu cidla pomocou LS
        monitor_count = monitor_ls.lock(block_sensors)

        # signalizujeme, ze sme dokoncili KO pre monitor
        block_monitors.signal()

        # prebehne aktualizacia dat na danom monitore
        data_update(40-50) # teda 40-50 milisekund

        # odomkneme pristup k datam pre vlakna
        # vykonavajuce cinnost cidla
        monitor_ls.unlock(block_sensors)


def sensor():
    while True:
        # signalizujeme, ze chceme zapisat,
        # takze dalsie volanie wait nad block_monitors,
        # ktore vykona nejake monitor vlakno
        # bude blokujuce
        sensor_count = sensor_ls.lock(block_monitors)

        # zamedzime monitor vlaknam, aby prechadzali cez tento
        # semafor, ktory je v monitor vlaknach blokovany
        # prvym vlaknom, ktore vykona lightswitch lock
        # nad tymto semaforom
        block_sensor.wait()

        # vykoname zapis udajov, ktore cidlo nameralo
        # cas je iny pre kazde cidlo, ale kedze zapisuju paralelne,
        # tak v najhorsom pripade bude zapis trvat 25ms
        write_data(10-20 | 20-25) # cas v milisekundach

        # umoznime monitor vlaknam znovu blokovat cidla
        # dalsie wait volanie nad tymto semaforom uz nebude blokujuce
        block_sensor.signal()

        # odomkneme monitorom semafor, ale odomkneme ho
        # pomocou lightswitch, cize posledne cidlo musi
        # ukoncit zapis, potom mozu monitory pokracovat
        sensor_ls.unlock(block_monitors)

        # signalizujeme, ze cidlo zapisalo nejake udaje
        data_present.signal()

        # aktualizujeme namerane data kazdy 50-60 milisekund
        sleep(50-60)
