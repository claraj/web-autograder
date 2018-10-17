package week_3;

import com.google.common.base.Joiner;

import org.junit.Rule;
import org.junit.Test;
import org.junit.contrib.java.lang.system.TextFromStandardInputStream;

import java.io.BufferedReader;
import java.io.FileReader;
import java.lang.reflect.Method;

import static org.junit.Assert.*;
import static org.junit.contrib.java.lang.system.TextFromStandardInputStream.emptyStandardInputStream;

public class Question_4_Reduce_RepetitionTest {

    // This one is tricky to test since student must decide how to restructure the program.
    // This is not a particularly good test. Students, if you are reading this, the instructor is going
    // to review your code and that's going to be the major factor in your grade for this assignment.
    // There are some tricks you can use to get around the line-counting code :)

    @Test(timeout = 3000)
    public void testCoffeeShopFileSize() throws Exception {

        // Test to see if the number of lines of code in the file got smaller...
        // The sort of test you would probably only ever write for checking student code :)

        // Yes, you can probably trick this test as well.

        Joiner joiner = Joiner.on(System.getProperty("file.separator"));
        String path = joiner.join("src", "main", "java", "week_3", "Question_4_Reduce_Repetition.java");   // yuck for the absolute file path. Also yuck for not checking if there is a library method to join parts of the path.
        BufferedReader reader = new BufferedReader(new FileReader(path));

        int loc = 0;
        String line;

        // Ignore comments, and count lines of code.

        boolean inBlockComment = false;  // Flag to identify if line is part of multi-line comment.

        while ( (line = reader.readLine()) != null ){

            line = line.trim();

            if (line.startsWith("/*")) {    // todo this doesn't catch  /* comments written like this */
                inBlockComment = true;
                // Does this comment start and end on the same line?
                if (line.contains("*/")) {
                    inBlockComment = false;
                }
            }

            if (line.endsWith("*/")) { inBlockComment = false; }

            if (inBlockComment) { continue; }

            if (line.startsWith("//")) {}  //ignore

            else if (line.length() == 0) {}  // empty line, ignore

            else {
                loc++;
            }
        }

        // Original file had 33 lines of code.
        int originalLoc = 33;

        System.out.println(String.format("The original program had %d lines of code. Your program now has %d lines of code", originalLoc, loc));
        assertTrue("Your version of this program would be expected to have less lines of code than the original. " +
                "\nOnly lines of code are counted, comments are not counted - write lots of comments!." +
                "\nYour solution will also be reviewed for clarity. Your program should still be clear and readable." +
                "\nIf you think your solution is correct and this method is not counting the lines correctly, please tell Clara. ", loc < originalLoc );
    }

    @Rule
    public final TextFromStandardInputStream systemInMock = emptyStandardInputStream();

    @Test(timeout = 3000)
    public void testCoffeeShop() throws Exception {

        systemInMock.provideLines("4", "12");   // Twelve drinks at $4 each, or 4 drinks at $12 each... doesn't matter what order the user enters them, math is the same.

        Class coffee = Class.forName("week_3.Question_4_Reduce_Repetition");
        Method[] methods = coffee.getMethods();

        // Any methods that take a String argument, like the name of a drink? Expect there to be only one matching method.

        for (Method m: methods) {

            Class[] paramTypes = m.getParameterTypes();
            if (paramTypes.length > 0 && paramTypes[0] == String.class) {
                System.out.println("The test found a method that takes a single String argument, the method name is " + m);

                // Call this method
                try {
                    Question_4_Reduce_Repetition q4 = new Question_4_Reduce_Repetition();
                    double sales = (double) m.invoke(q4, "Coffee");
                    assertEquals((int) sales, 4 * 12);
                    System.out.println("** Found a method that appears to have the expected sales-calculating behavior");
                    return;

                } catch (Exception e) {
                    // Not a problem if the method being sought hasn't been found yet.
                    fail("Error trying to call" + m.getName() + " to calculate sales total for a drink. " +
                            "\nMake sure you only ask the user two questions - the price of a drink, and the total sales for that drink.");
                }
            }
        }

        fail("Looked for methods that take a String argument (name of drink), and return a double (total sales for that drink, calculated from user input)." +
                "\nDid not find exactly one method with sales calculating behavior. " +
                "\nThere are other ways to solve this problem, so this may not be an error in your code. " +
                "\nYour code will be reviewed and graded by a human. " +
                "\nIf you are confident in your solution, you can ignore this test failure. ");

    }

}