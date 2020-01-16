// 
// Decompiled by Procyon v0.5.36
// 

package com.trendmicro;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.charset.Charset;
import java.io.IOException;
import javax.servlet.ServletException;
import org.springframework.expression.Expression;
import org.springframework.expression.ExpressionParser;
import org.springframework.expression.spel.standard.SpelExpressionParser;
import java.nio.charset.StandardCharsets;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;

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