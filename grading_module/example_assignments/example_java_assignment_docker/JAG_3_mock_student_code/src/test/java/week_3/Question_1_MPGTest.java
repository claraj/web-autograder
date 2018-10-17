package week_3;

import org.junit.Test;

import java.lang.reflect.Method;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;
import static test_utils.MethodUtil.*;

public class Question_1_MPGTest {
    
    
    private double delta = 0.00001;
    
    
    @Test(timeout=3000)
    public void testMPGCalculations() {

        // So this method doesn't exist when this test is being written.
        
        // Use reflection to find and call the new
        // mpg method that the student has written.

        Method mpg = findMethod("week_3.Question_1_MPG", "mpg", new Class[]{double.class, double.class});

        try {

            // Create a new object for our class
            Question_1_MPG q2 = new Question_1_MPG();

            // Call the discovered mpg method with some example arguments

            // 10 miles, 4 gallons of gas, should be 10/4 = 2.5 MPG
            Object result = mpg.invoke(q2, 10, 4);

            // Returns the correct type?
            assertTrue("Make sure you return a double number from the mpg method", result instanceof Double);

            // Convert the value to a double
            double resultDouble = (double) result;
            // Check if it is the expected values
            assertEquals("For 10 miles driven, and 4 gallons of gas, the MPG should be 2.5", resultDouble, 2.5, delta);

            // Check again, with some other example values
            // 300 miles, 4.1 gallons of gas should return 300/4.1 = 73.170731
            result = mpg.invoke(q2, 300, 4.1);
            resultDouble = (double) result;
            assertEquals("\"For 300 miles driven, and 4.1 gallons of gas, the MPG should be 73.170731. " +
                    "\nDo not use any number formatting or rounding in your method. Return the exact calculated value.", resultDouble, 73.170731, delta);


        } catch (Exception e) {
            // Catch for method.invoke. Will fail if the wrong number of method arguments are given, or are not the correct types
            fail("Check that the mpg method takes two double arguments, the miles driven, and gas used, in that order.");
        }

    }

    
}