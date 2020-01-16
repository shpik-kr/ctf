// 
// Decompiled by Procyon v0.5.36
// 

package com.trendmicro;

import java.util.Arrays;
import java.io.ObjectStreamClass;
import java.io.IOException;
import java.io.InputStream;
import javax.servlet.ServletInputStream;
import java.io.ObjectInputStream;

public class CustomOIS extends ObjectInputStream
{
    private static final String[] whitelist;
    
    static {
        whitelist = new String[] { "com.trendmicro.Person" };
    }
    
    public CustomOIS(final ServletInputStream is) throws IOException {
        super((InputStream)is);
    }
    
    public Class<?> resolveClass(final ObjectStreamClass des) throws IOException, ClassNotFoundException {
        if (!Arrays.asList(CustomOIS.whitelist).contains(des.getName())) {
            throw new ClassNotFoundException("Cannot deserialize " + des.getName());
        }
        return super.resolveClass(des);
    }
}