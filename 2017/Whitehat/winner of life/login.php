  <body>

    <div class="container">

      <form class="form-signin" method='post' action='login_check.php'>
        <h2 class="form-signin-heading">Please sign in</h2>
        <label class="sr-only">USER ID</label>
        <input name="userid" class="form-control" placeholder="USER ID" required autofocus>
        <label for="inputPassword" class="sr-only">Password</label>
        <input type="password" name="userpw" class="form-control" placeholder="Password" required>
        <div class="checkbox">
          <label>
            <input type="checkbox" value="remember-me"> Remember me
          </label>
        </div>
        <button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
      </form>

    </div> <!-- /container -->


    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="dist/js/ie10-viewport-bug-workaround.js"></script>
  </body>