package week_3;

import org.junit.Test;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

import static org.junit.Assert.*;
import static test_utils.MethodUtil.findMethod;

public class Question_2_Wear_A_HatTest {

    @Test
    public void doYouNeedAHatTodayAbove40() {
        findAndInvokeHatMethod(40.0000001, false);
        findAndInvokeHatMethod(70.0, false);
    }



    @Test
    public void doYouNeedAHatTodayAt40() {
        findAndInvokeHatMethod(40.0, true);
    }


    @Test
    public void doYouNeedAHatTodayBelow40() {
        findAndInvokeHatMethod(39.9999, true);
        findAndInvokeHatMethod(20, true);
        findAndInvokeHatMethod(-10, true);
    }


    private void findAndInvokeHatMethod(double tempIn, boolean expectedOut) {

        Method method = findMethod("week_3.Question_2_Wear_A_Hat", "doYouNeedAHat", new Class[]{double.class});

        Question_2_Wear_A_Hat q2 = new Question_2_Wear_A_Hat();

        try {

            boolean wearHat = (boolean) method.invoke(q2, tempIn);
            assertEquals("Your doYouNeedAHat method, called with the temperature '"
                            + tempIn
                            + "' is expected to return "
                            + expectedOut
                            + ".\n",
                    expectedOut, wearHat);

        } catch (InvocationTargetException ie) {
            String message = "When called with the double '" + tempIn + "' your method threw a " + ie.getTargetException().getClass().toString() + ", " + ie.getTargetException().getMessage();
            fail(message);
        } catch (ClassCastException e) {
            fail("Is your method returning the correct type of data? It should return a boolean.");
        } catch (Exception e) {
            fail("This exception was thrown: " + e.getMessage());
        }

    }
}
