package com.trendmicro;

import java.util.Arrays;
import java.io.ObjectStreamClass;
import java.io.IOException;
import java.io.InputStream;
import java.io.ObjectInputStream;
import java.io.FileInputStream;

public class CustomOIS extends ObjectInputStream
{
    private static final String[] whitelist;
    
    static {
        whitelist = new String[] { "com.trendmicro.Person" };
    }
    
    public CustomOIS(final FileInputStream is) throws IOException {
        super((InputStream)is);
    }
    
    public Class<?> resolveClass(final ObjectStreamClass des) throws IOException, ClassNotFoundException {
        if (!Arrays.asList(CustomOIS.whitelist).contains(des.getName())) {
            throw new ClassNotFoundException("Cannot deserialize " + des.getName());
        }
        // System.out.print(des);
        return super.resolveClass(des);
    }
}
