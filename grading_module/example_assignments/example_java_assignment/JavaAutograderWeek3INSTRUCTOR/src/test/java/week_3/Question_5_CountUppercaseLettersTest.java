package week_3;

import org.junit.Test;

import java.lang.reflect.Array;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Arrays;

import static org.junit.Assert.*;
import static test_utils.MethodUtil.findMethod;

public class Question_5_CountUppercaseLettersTest {


    @Test(timeout=3000)
    public void testCountUpperCaseNoUpperCaseLetters() {
        invokeCountUppercase(new String[]{ "a", "b", "c"}, 0);
        invokeCountUppercase(new String[]{ "a", "b", "c", "5"}, 0);
        invokeCountUppercase(new String[]{}, 0);
        invokeCountUppercase(new String[]{ "5", "%", "6", "\t"}, 0);
    }


    @Test(timeout=3000)
    public void testCountUpperCaseUpperCaseLetters() {
        invokeCountUppercase(new String[]{ "a", "B", "c"}, 1);
        invokeCountUppercase(new String[]{ "A", "B", "C", "5"}, 3);
        invokeCountUppercase(new String[]{ "J", "A", "V", "A"}, 4);
        invokeCountUppercase(new String[]{ "5", "E", "%", "G", "\t", "g"}, 2);
    }



    private void invokeCountUppercase(String[] input, int expectedOut) {

        Method method = findMethod("week_3.Question_5_Count_Uppercase_Letters", "countUppercase", new Class[]{String[].class});

        Question_5_Count_Uppercase_Letters q5 = new Question_5_Count_Uppercase_Letters();

        try {

            int uppercaseCount = (int) method.invoke(q5, (Object) input);   // Cast to Object so the String array is not interpreted as varargs.
            assertEquals("Your stringToIntArray method, called with the Array '"
                            + Arrays.toString(input)
                            + "' is expected to return "
                            + expectedOut
                            + ".\n",
                    expectedOut, uppercaseCount);

        } catch (InvocationTargetException ie) {
            String message = "When called with the Array '" + Arrays.toString(input) + "' your method threw a " + ie.getTargetException().getClass().toString() + ", " + ie.getTargetException().getMessage();
            fail(message);
        } catch (ClassCastException e) {
            fail("Is your method returning the correct type of data? It should return an int.");
        } catch (Exception e) {
            fail("This exception was thrown: " + e.getMessage());
        }
        
    }
    
    
}