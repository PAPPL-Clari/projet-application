/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 */

package com.mycompany.projetapplicna;

import java.util.ResourceBundle;
import java.util.*;
import java.net.URL;
import java.net.HttpURLConnection;

/**
 *
 * @author Larissa
 */
public class ProjetAppliCNA {

    public static void main(String[] args) {
        try{
            // Get Properties file
            ResourceBundle properties = ResourceBundle.getBundle(ProjetAppliCNA.class.getPackage().getName() + ".api");

            // USE config parameters
            String key = properties.getString("key");
            String secret = properties.getString("secret");
            String url = "https://centraliens-nantes.org/api/v2/customer/me/whoami?access_secret=${"+ secret +"}&access_id=${"+ key +"}";
            URL conn = new URL(url);
            
            HttpURLConnection connection = (HttpURLConnection) conn.openConnection();
            connection.setRequestMethod("GET");
            connection.connect();
            
            int responseCode = connection.getResponseCode();
            
            if (responseCode != 200){
                throw new RuntimeException("HttpResponseCode: "+ responseCode);
            }else{
                StringBuilder informationString = new StringBuilder();
                Scanner scanner = new Scanner(conn.openStream());
                
                while(scanner.hasNext()){
                    informationString.append(scanner.nextLine());
                }
                
                scanner.close();
                
                System.out.println(informationString);
                
            }
        }
        catch(Exception e){
            e.printStackTrace();
        }
        
    }
}
