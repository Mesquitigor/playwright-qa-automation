import java.io.*;
import java.net.*;
import com.google.gson.*;

class Main {
  public static int fetchAndCountPosts() throws Exception {
    System.setProperty("http.agent", "Chrome");
    Reader in = new InputStreamReader(
        new URL("https://coderbyte.com/api/challenges/json/all-posts").openStream());
    int count = new Gson().fromJson(in, JsonArray.class).size();
    in.close();
    return count;
  }

  public static void main(String[] args) throws Exception {
    System.out.println("Number of posts: " + fetchAndCountPosts());
  }
}
