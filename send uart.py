import serial
import struct
import time
class FirmwareHeader:
    def __init__(self, version, num_blocks, blocksize, crc):
        self.version = version
        self.num_blocks = num_blocks
        self.blocksize = blocksize
        self.crc = crc

def parse_header_from_bytes(header_bytes):
    # Разбор байтового потока в переменные заголовка
    version, num_blocks, blocksize, crc = struct.unpack("<HHBB", header_bytes)

    # Создание объекта заголовка
    header = FirmwareHeader(version=version, num_blocks=num_blocks, blocksize=blocksize, crc=crc)

    return header

def send_file_via_serial(file_path, com_port):
    try:
        # Открытие COM-порта
        ser = serial.Serial(com_port, baudrate=921600, timeout=10)
        print("COM-порт успешно открыт.")

        with open(file_path, "rb") as file:
            data = file.read()

        # Создание заголовка
        header = parse_header_from_bytes(data[:6])
        ser.write(data[:6])
        char = ser.readline()
        print(char)
        
        data = data[6:]
        # Упаковка заголовка в байтовую последовательность
        for i in range(header.num_blocks):
            block = data[i*(header.blocksize+1):(i+1)*(header.blocksize+1)]
            ser.write(block)
            print("{} bytes sent {}".format(len(block), block[-5:-1]))
            response = ser.readline()
            print(response)
            response = ser.readline()  # Ожидание "OK" от получателя
            if response != b'OK\n':
                print("Ошибка: Не получен сигнал 'OK'")
                print(response)
        # Отправка заголовка по COM-порту
        print("ВСЕ")
        while True:
            print(ser.readline())

        # Отправка данных по COM-порту
        ser.write(data)
        print("Файл успешно отправлен.")

        # Закрытие COM-порта
        ser.close()
        print("COM-порт успешно закрыт.")

    except serial.SerialException as e:
        print(f"Произошла ошибка при работе с COM-портом: {e}")

# Пример использования
#file_path = input("Введи файл:")
com_port = "COM3"  # Номер COM-порта
file_path = r"C:\Users\user\source\repos\firmwareBuilder\firmwareBuilder\F303_new.bin"

send_file_via_serial(file_path, com_port)
