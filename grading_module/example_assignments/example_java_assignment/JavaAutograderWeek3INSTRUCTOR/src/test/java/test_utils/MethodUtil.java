package test_utils;

import java.lang.reflect.Method;

import static junit.framework.TestCase.fail;

/**
 * Created by Clara on 6/1/17.
 * Helper methods to find methods in classes under test. */

 public class MethodUtil {

    public static Method findMethod(String className, String methodName, Class[] parameters) {

        Class cl = null;
        Method method = null;

        // Create an object of our class under test
        try {
            cl = Class.forName(className);
        } catch (ClassNotFoundException e) {
            fail(String.format("Expected to find a class with name %s. Check if the name of the class was changed?", className));
        }

        // Find the method of the given name method
        try {
            method = cl.getMethod(methodName, parameters);
        } catch (NoSuchMethodException e) {

            String paramMsg = "these parameter types: ";
            if (parameters == null) {
                paramMsg += "no parameters";
            } else {
                for (Class c : parameters) {
                    paramMsg += c.getName() + " ";
                }
            }
            String message = String.format("Expected to find a public method with name %s and %s", methodName, paramMsg);
            fail(message);
        }

        return method;
    }
}
