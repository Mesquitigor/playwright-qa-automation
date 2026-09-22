import java.util.*;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import com.google.gson.*;

class Main {

  private static final String POSTS_URL =
      "https://coderbyte.com/api/challenges/json/all-posts";

  /**
   * GET the posts list from Coderbyte and return how many posts it contains.
   */
  public static int fetchAndCountPosts() {
    System.setProperty("http.agent", "Chrome");

    try {
      URL url = new URL(POSTS_URL);
      HttpURLConnection connection = (HttpURLConnection) url.openConnection();
      connection.setRequestMethod("GET");
      connection.setRequestProperty("User-Agent", "Chrome");

      BufferedReader reader = new BufferedReader(
          new InputStreamReader(connection.getInputStream()));
      StringBuilder response = new StringBuilder();
      String line;
      while ((line = reader.readLine()) != null) {
        response.append(line);
      }
      reader.close();
      connection.disconnect();

      JsonArray posts = new Gson().fromJson(response.toString(), JsonArray.class);
      return posts.size();
    } catch (Exception e) {
      e.printStackTrace();
      return 0;
    }
  }

  public static void main(String[] args) {
    int numberOfPosts = fetchAndCountPosts();
    System.out.println("Number of posts: " + numberOfPosts);
  }
}
