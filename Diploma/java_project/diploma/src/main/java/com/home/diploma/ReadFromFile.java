package com.home.diploma;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;

import javax.xml.bind.DatatypeConverter;

public class ReadFromFile {
	
	private static File file = new File("./GPS_output.out");
	private static InputStream fis;

	public static void main(String[] args) throws Exception {
		fis = new FileInputStream(file);
		byte[] result = new byte[(int)file.length()];
		fis.read(result);
		String hexString = DatatypeConverter.printHexBinary(result);
		fis.close();
		String[] messages = hexString.split("(?=A0A2)");
		for (String message : messages) {
			if (!message.substring(message.length()-4).equals("B0B3")) continue;
			if (message.substring(8, 10).equals("1C")) {
				System.out.println("Measurements taken at: " + hexToDouble(message.substring(22, 38)));
				System.out.println("Satellite ID: " + Integer.parseInt(message.substring(20, 22), 16));
				System.out.println("Pseudorange: " + hexToDouble(message.substring(38, 54)));
				System.out.println("");
			}
			
		}
	}
	
	public static double hexToDouble(String hex) {
		String newHex = hex.substring(8) + hex.substring(0, 8);
		long l = Long.parseLong(newHex, 16);
		double d = Double.longBitsToDouble(l);
        return d;
	}
	
	public static float hexToFloat(String hex) {
		String newHex = hex.substring(6) + hex.substring(4, 6) + hex.substring(2, 4) + hex.substring(0, 2);
		Long l = Long.parseLong(newHex, 16);
		Float f = Float.intBitsToFloat(l.intValue());
		return f;
	}
}
