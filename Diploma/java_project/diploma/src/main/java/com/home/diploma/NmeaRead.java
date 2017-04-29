package com.home.diploma;

import java.nio.charset.StandardCharsets;
import java.util.Scanner;

import jssc.SerialPort;
import jssc.SerialPortEvent;
import jssc.SerialPortEventListener;
import jssc.SerialPortException;

public class NmeaRead {

    private static SerialPort serialPort;

    public static void main(String[] args) {
        serialPort = new SerialPort("/dev/tty.usbserial");
        Scanner keyboard = new Scanner(System.in);
        try {
            serialPort.openPort();
            System.out.println("opened port");
            serialPort.setParams(SerialPort.BAUDRATE_4800, SerialPort.DATABITS_8, SerialPort.STOPBITS_1, SerialPort.PARITY_NONE);
            System.out.println("set params");
            serialPort.setEventsMask(SerialPort.MASK_RXCHAR);
            System.out.println("started reading");
            serialPort.addEventListener(new EventListener());
            if (keyboard.nextLine().equals("stop")) {
            	serialPort.closePort();
            	System.out.println("stopped reading");
            	keyboard.close();
            }
        }
        catch (SerialPortException ex) {
            System.out.println(ex);
        }
    }

    private static class EventListener implements SerialPortEventListener {

        public void serialEvent(SerialPortEvent event) {
            if(event.isRXCHAR() && event.getEventValue() > 0){
                try {
                    byte[] buffer = serialPort.readBytes(event.getEventValue());
                    System.out.print(new String(buffer, StandardCharsets.US_ASCII));
                }
                catch (SerialPortException ex) {
                    System.out.println(ex);
                }
            }
        }
    }
}