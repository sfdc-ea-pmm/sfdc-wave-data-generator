package pmmtech;

import java.util.Calendar;
import java.util.Locale;
import java.util.Random;

import static java.util.Calendar.*;

import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;

/**
 * Helper
 */
public class Helper {

    public static int getDiffYears(Date first, Date last) {
        Calendar a = getCalendar(first);
        Calendar b = getCalendar(last);
        int diff = b.get(YEAR) - a.get(YEAR);
        if (a.get(MONTH) > b.get(MONTH) || 
            (a.get(MONTH) == b.get(MONTH) && a.get(DATE) > b.get(DATE))) {
            diff--;
        }
        return diff;
    }
    
    public static Calendar getCalendar(Date date) {
        Calendar cal = Calendar.getInstance(Locale.US);
        cal.setTime(date);
        return cal;
    }

    public static List<Integer> getRandomIndexesList(int listSize, int totalItemsToPick){
        HashMap<Integer, Boolean> pickedIndexes = new HashMap<Integer, Boolean>();
        List<Integer> lstRandomIndexes = new ArrayList<Integer>();
        Random rand = new Random(); 
        int i = 0;
        
        while (i < totalItemsToPick) {
            // take a random index between 0 to size  
            // of given List 
            int randomIndex = rand.nextInt(listSize);
            if (!pickedIndexes.containsKey(randomIndex)) {
                pickedIndexes.put(randomIndex, true);
                i++;
            }
        }

        lstRandomIndexes.addAll(pickedIndexes.keySet());
        
        return lstRandomIndexes;
    }

    public static String[] concatArrays(String[] jobsA, String[] jobsB){
        String[] result = new String[jobsA.length + jobsB.length];
        int currentPos = 0;
        System.arraycopy(jobsA, 0, result, currentPos, jobsA.length);
        currentPos += jobsA.length;
        System.arraycopy(jobsB, 0, result, currentPos, jobsB.length);

        return result;
    }

    public static int getRandomNumberInRange(int min, int max) {

		if (min >= max) {
			throw new IllegalArgumentException("max must be greater than min");
		}

		Random r = new Random();
		return r.nextInt((max - min) + 1) + min;
	}
}