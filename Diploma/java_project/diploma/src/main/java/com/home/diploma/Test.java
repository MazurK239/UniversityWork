package com.home.diploma;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.nio.ByteBuffer;
import java.sql.Date;
import java.util.Scanner;

import javax.xml.bind.DatatypeConverter;

import jssc.SerialPort;
import jssc.SerialPortEvent;
import jssc.SerialPortEventListener;
import jssc.SerialPortException;

public class Test {
	
	public static void main(String[] args) {
		byte[] tmp = new byte[4];
		byte[] message = DatatypeConverter.parseHexBinary("A0A200140703BD0215492408000122310000472814D4DAEF0598B0B3");
		for (int i = 0; i < 4; i++) {  
			tmp[i] = message[10 - i];			
		}
		float timeInMessage = ByteBuffer.wrap(tmp).getFloat();
		System.out.println(timeInMessage);
	}
	
	
}
