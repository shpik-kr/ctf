package com.trendmicro;

import org.xml.sax.SAXException;
import javax.xml.parsers.ParserConfigurationException;
import java.io.IOException;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.w3c.dom.Document;
import javax.xml.parsers.DocumentBuilder;
import java.io.InputStream;
import javax.xml.parsers.DocumentBuilderFactory;
import java.io.ByteArrayInputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.io.*;

public class Person implements Serializable
{
    public String name;
    private static final long serialVersionUID = -559038737L;
    
    public Person(final String name) {
        this.name = name;
    }
    
    private void readObject(final ObjectInputStream aInputStream) throws ClassNotFoundException, IOException, ParserConfigurationException, SAXException {
        final int paramInt = aInputStream.readInt();
        final byte[] arrayOfByte = new byte[paramInt];
        aInputStream.read(arrayOfByte);
        final ByteArrayInputStream localByteArrayInputStream = new ByteArrayInputStream(arrayOfByte);
        final DocumentBuilderFactory localDocumentBuilderFactory = DocumentBuilderFactory.newInstance();
        localDocumentBuilderFactory.setNamespaceAware(true);
        final DocumentBuilder localDocumentBuilder = localDocumentBuilderFactory.newDocumentBuilder();
        final Document localDocument = localDocumentBuilder.parse(localByteArrayInputStream);
        final NodeList nodeList = localDocument.getElementsByTagName("tag");
        final Node node = nodeList.item(0);
        this.name = node.getTextContent();
    }
    private void writeObject(final ObjectOutputStream aOutputStream) throws ClassNotFoundException, IOException, ParserConfigurationException, SAXException {
        aOutputStream.writeInt(name.length());
        aOutputStream.writeBytes(name);
    }
}
