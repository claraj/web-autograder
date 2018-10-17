package test_utils;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

/**
 * Created by clara on 6/1/17.
 */
public class PrintUtils {

    static PrintStream out;
    static ByteArrayOutputStream bytesOut;

    static PrintStream originalOut = System.out;

    public static void catchStandardOut() {

        bytesOut = new ByteArrayOutputStream();
        out = new PrintStream(bytesOut);
        System.setOut(out);

    }

    public static String resetStandardOut() {
        System.setOut(originalOut);
        return bytesOut.toString();
    }

}
