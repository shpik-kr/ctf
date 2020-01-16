// 
// Decompiled by Procyon v0.5.36
// 

package com.trendmicro.jail;

import java.io.Reader;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.Serializable;

public class Flag implements Serializable
{
    static final long serialVersionUID = 6119813099625710381L;
    
    public static void getFlag() throws Exception {
        final ProcessBuilder processBuilder = new ProcessBuilder(new String[0]);
        processBuilder.command("/TMCTF2019/flagbin");
        final Process process = processBuilder.start();
        final BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        final String flag = reader.readLine();
        throw new Exception(flag);
    }
}