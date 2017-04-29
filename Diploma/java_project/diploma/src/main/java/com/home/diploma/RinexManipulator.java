package com.home.diploma;

import java.io.FileOutputStream;
import java.io.FileNotFoundException;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;

public class RinexManipulator {

	private static FileOutputStream fos;
	
	public static void createNewFile(String filename) {
//		ZonedDateTime utc = ZonedDateTime.now(ZoneOffset.UTC);
//		String filename = "./home" + utc.getYear() + utc.getMonthValue() + utc.getDayOfMonth() + ".rinex";
		try {
			fos = new FileOutputStream(filename);
			System.out.println("created file");
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
	}
	
	public static void addLine(String line) {
		try {
			fos.write(line.getBytes());
		} catch (Exception e) {
//			do nothin'
		}
	}

}
