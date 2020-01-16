package com.trendmicro;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.ServletInputStream;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;

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