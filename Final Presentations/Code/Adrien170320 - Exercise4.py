<!DOCTYPE html>

<html lang="en" style="height: 100%">
    <head>
        <meta charset="utf-8">
        <title>Adrien170320 - Exercise4.py : /home/Adrien170320/LDA/Scripts/Adrien170320 - Exercise4.py : Editor : Adrien170320 : PythonAnywhere</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="Adrien170320 - Exercise4.py : /home/Adrien170320/LDA/Scripts/Adrien170320 - Exercise4.py : Editor : Adrien170320 : PythonAnywhere">
        <meta name="author" content="PythonAnywhere LLP">
        <meta name="google-site-verification" content="O4UxDrfcHjC44jybs2vajc1GgRkTKCTRgVzeV6I9V14" />


        <!-- Le styles -->
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,300i,400,400i,700,700i" />

        <link rel="stylesheet" href="/static/CACHE/css/output.ff34947502d6.css" type="text/css" media="screen">
        <link rel="stylesheet" href="/static/CACHE/css/output.b9a4961a16f7.css" type="text/css"><link rel="stylesheet" href="/static/CACHE/css/output.135dadead6d9.css" type="text/css" media="screen">

        <!-- Le javascript -->
        <script type="text/javascript">
            var Anywhere = {};
            Anywhere.urls = {};
            Anywhere.csrfToken = "25iw3SJUeCjnoWG2dubPH5yuemfXXkzKh9ezCgIVQ2nVqozCb0JKyL3SPVhDNU3H";
        </script>
        <script src="/static/CACHE/js/output.9912b9c89b96.js"></script>
        

        <script src="/static/CACHE/js/output.ce8d62eca661.js"></script>
        
    <script type="text/javascript">
      $(document).ready(function() {
        $.extend(Anywhere.urls, {
          file: "/user/Adrien170320/files/home/Adrien170320/LDA/Scripts/Adrien170320%20-%20Exercise4.py",
          check_hash: "/user/Adrien170320/files/home/Adrien170320/LDA/Scripts/Adrien170320%20-%20Exercise4.py",
          update_editor_mode_preference: "/user/Adrien170320/account/update_editor_mode_preference",
          console_api: "/api/v0/user/Adrien170320/consoles/",
        });
        var filename = "/home/Adrien170320/LDA/Scripts/Adrien170320 \u002D Exercise4.py";
        var hash = "60a6adf99591a1bd71bbde2cf5c6046f";
        var interpreter = "python3.10";

        
            Anywhere.Editor.InitializeAce(ace, Anywhere.urls, filename, hash, interpreter, "pythonanywhere.com");
            $("#id_keybinding_mode_select").val("normal");
            $("#id_keybinding_mode_select").trigger("change");
        
        var consoleVisible = true;
        Anywhere.Editor.splitPanes(consoleVisible);

        Anywhere.WebAppControl.initialize();
        Anywhere2.initializeFileSharingOptions(
          $('#id_file_sharing_options')[0],
          {
            url: "/api/v0/user/Adrien170320/files/sharing/",
            csrfToken: "25iw3SJUeCjnoWG2dubPH5yuemfXXkzKh9ezCgIVQ2nVqozCb0JKyL3SPVhDNU3H",
            path: "/home/Adrien170320/LDA/Scripts/Adrien170320 \u002D Exercise4.py"
          }
        );

      });
    </script>

        

    </head>

     <body style="height:100%;">
       <div style="min-height: 100%; position: relative;">
        
        
  




  <nav class="navbar navbar-default fullscreen-main-navbar">
    <div class="navbar-header">
      <a class="navbar-brand" href="/">
        <img id="id_logo" src="/static/anywhere/images/PA-logo-snake-only.svg" height="100%" />
      </a>
    </div>

    <div class="extra-nav-content">
      

  <div id="id_editor_toolbar">

    <div class="pull-left">
      <span id="id_breadcrumbs_div"><a class="breadcrumbs_link breadcrumb_entry" href="/user/Adrien170320/files/" target="_parent">/</a><a class="breadcrumbs_link breadcrumb_entry" href="/user/Adrien170320/files/home" target="_parent">home</a><span class="breadcrumb_entry">/</span><a class="breadcrumbs_link breadcrumb_entry" href="/user/Adrien170320/files/home/Adrien170320" target="_parent">Adrien170320</a><span class="breadcrumb_entry">/</span><a class="breadcrumbs_link breadcrumb_entry" href="/user/Adrien170320/files/home/Adrien170320/LDA" target="_parent">LDA</a><span class="breadcrumb_entry">/</span><a class="breadcrumbs_link breadcrumb_entry" href="/user/Adrien170320/files/home/Adrien170320/LDA/Scripts" target="_parent">Scripts</a><span class="breadcrumb_entry">/</span><wbr><span class="breadcrumb_entry breadcrumb_terminal">Adrien170320 - Exercise4.py</span></span>

      <span>
        <span id="id_unsaved_changes_spacer">
          <span id="id_unsaved_changes" class="pa_hidden muted">(unsaved changes)</span>
        </span>
      </span>
    </div>

    <div id="id_editor_messages" class="pull-left">
      

    </div>

    <div class="pull-right">
      <div id="id_editor_buttons_right" class="form-inline">
        <span id="id_save_error" class="pa_hidden alert alert-danger">Error saving.</span>
        <img src="/static/anywhere/images/spinner-small.gif" class="pa_hidden" id="id_save_spinner" />
        
          <span id="id_keyboard_shortcuts"><a href="#">Keyboard shortcuts:</a></span>
          <select id="id_keybinding_mode_select" class="form-control input-sm">
            <option value="normal">Normal</option>
            <option value="vim">Vim</option>
          </select>
        
        <button id="id_display_sharing_options" class="btn btn-default" data-toggle="modal" data-target="#id_file_sharing_modal" title="Get a URL to share this file">
          <span class="glyphicon glyphicon-paperclip" aria-hidden="true"></span>
          Share
        </button>
        
          <button id="id_save" class="btn btn-success" title="Save (Ctrl + S)">
            <span class="glyphicon glyphicon-floppy-disk" aria-hidden="true"></span>
            Save
          </button>
          <button id="id_save_as" class="btn btn-default" title="Save As">Save as...</button>
        
        
          <button class="btn btn-info run_button" title="Save &amp; Run (Ctrl + R)">
            <span><code>&gt;&gt;&gt;</code></span>
            Run
          </button>
        

        
      </div>
    </div>

  </div>


    </div>

    <div class="dropdown fullscreen-hamburger fullscreen-mini-nav">
      <button type="button" class="navbar-toggle" data-toggle="dropdown"  role="button" aria-haspopup="true" aria-expanded="false">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <ul class="dropdown-menu pull-right">
        
  <li class=""><a id="id_dashboard_link" href="/user/Adrien170320/">Dashboard</a></li>
  <li class=""><a id="id_consoles_link" href="/user/Adrien170320/consoles/">Consoles</a></li>
  <li class=""><a id="id_files_link" href="/user/Adrien170320/files/home/Adrien170320">Files</a></li>
  <li class=""><a id="id_web_app_link" href="/user/Adrien170320/webapps/">Web</a></li>
  <li class=""><a id="id_tasks_link" href="/user/Adrien170320/tasks_tab/">Tasks</a></li>
  <li class=""><a id="id_databases_link" href="/user/Adrien170320/databases/">Databases</a></li>


        
<li class=""><a href="" target="_parent" class="feedback_link">Send feedback</a></li>


<li class=""><a href="/forums/" target="_parent" class="forums_link">Forums</a></li>
<li class=""><a href="https://help.pythonanywhere.com/" target="_parent" class="help_link">Help</a></li>
<li class=""><a href="https://blog.pythonanywhere.com/" target="_parent" class="blog_link">Blog</a></li>

  
  <li class=""><a href="/user/Adrien170320/account/" target="_parent" class="account_link">Account</a></li>
  <li class="">
    <form action="/logout/" method="POST" target="_parent">
      <input type="hidden" name="csrfmiddlewaretoken" value="25iw3SJUeCjnoWG2dubPH5yuemfXXkzKh9ezCgIVQ2nVqozCb0JKyL3SPVhDNU3H">
      <button type="submit" class="btn-link logout_link">Log out</button>
    </form>
  </li>


      </ul>
    </div>

  </nav>



        
    


        
  <div>
    <div id="id_ide_split_panes">

      
        <div id="id_editor"># Dans cet exercice, vous devrez trouver - en scrapant - l&#39;article en vigueur le plus long du code suivant:

code = &#39;Code de l&#39;artisanat&#39;

#Pour ce faire, utilisez le scrapper Legifrance présent sur Github. L&#39;URL du code se trouve dans le dictionnaire Ligne 13.

In [18]: for code in code_artisanat:  # I am iterating through all codes, but be sure to change that to a single one if you are only interested in one
    ...:     print(code)  # Print to keep track of what code is being parsed
    ...:     driver.get(&quot;https://www.legifrance.gouv.fr/&quot; + codes[code])  # Get the specific law code we are interested, using the dict defined above
    ...:     soup = BeautifulSoup(driver.page_source)  # Read HTML, pass it to a soup object
    ...:     set_articles = soup.find_all(&quot;a&quot;, string=re.compile(&quot;^Article&quot;))  # Find all articles in the code, by looking for all links whose text starts
    ...: with Article
    ...:     for article in set_articles:  # Iterate over articles one by one
    ...:         legiarti_match = re.search(&quot;LEGIARTI.*?#&quot;, article.get(&quot;href&quot;))
    ...:         if legiarti_match:
    ...:             legiarti = legiarti_match.group()[:-1]
    ...:         else:
    ...:             continue
    ...:         driver.get(&quot;https://www.legifrance.gouv.fr/codes/article_lc/&quot; + legiarti)  # Go to that URL
    ...:         time.sleep(1)  # Wait a bit
    ...:         article_num = driver.find_element(By.CLASS_NAME, &quot;name-article&quot;).text  # Look for the full name of the article, which is an element of cla
    ...: ss &quot;name-article&quot;
    ...:         article_text = driver.find_elements(By.CLASS_NAME, &quot;content&quot;)[2].text  # The content of the article, we know from the inspector that this
    ...: is the third element of class &quot;content&quot;
    ...:         temp_list = [code, article_num, article_text]  # We create our first list with all data collected so far, put some placeholders for types
    ...: of citations
    ...:         if len(driver.find_elements(By.XPATH, &quot;.//button[@data-articleid=&#39;&quot; + legiver + &quot;&#39;]&quot;)) &gt; 1:  # Looking for the &quot;Liens Relatifs&quot; tab, by co
    ...: unting number of tabs; if more than 1 (the &quot;Versions&quot; tab), then there is a &quot;Lien Relatifs&quot; tab
    ...:                 driver.find_elements(By.XPATH, &quot;.//button[@data-articleid=&#39;&quot; + legiver + &quot;&#39;]&quot;)[1].click()  # We then click on it
    ...:                 time.sleep(1)  # And wait a bit
    ...:         data_scrapped.append(temp_list)
    ...:     driver.close ()
    ...:
Code de l&#39;artisanat

In [19]: df = pd.DataFrame(data_scrapped, columns=[&quot;Code&quot;, &quot;Art&quot;, &quot;Text&quot;])

In [20]: df.to_csv(&quot;Adrien17020.csv&quot;, encoding=&quot;utf8&quot;)

In [22]: df[&quot;Length&quot;] = df[&quot;Text&quot;].apply(len)

In [23]: max_article = df.loc[df[&quot;Length&quot;].idxmax()]


In [25]: print (max_article)
Code                                    Code de l&#39;artisanat
Art                                              Article 19
Text      I.-L&#39;installation de l&#39;assemblée générale des ...
Length                                                10586
Name: 22, dtype: object


</div>
      

      <div id="id_ide_console">
        
          <iframe src="/user/Adrien170320/consoles/27921799/frame/" id="id_console" name="console" class="soft_keyboard_sensitive">
          </iframe>
        
      </div>

    </div>

    <div id="id_go_to_line_dialog" class="pa_hidden">
      <p class="form-inline">Line number: <input id="id_go_to_line_dialog_input" /></p>
      <div class="dialog_buttons">
        <button class="btn btn-default" id="id_go_to_line_dialog_ok_button">Go</button>
        <button class="btn btn-default" id="id_go_to_line_dialog_close_button">Close</button>
      </div>
    </div>

    <div id="id_file_changed_on_disk" class="pa_hidden">
      <p>Are you sure you want to save it?  Alternatively, you could re-open it in a new tab to check differences</p>
      <div class="dialog_buttons">
        <button id="id_force_save" class="btn btn-danger">Force Save</button>
        <button id="id_cancel_save" class="btn btn-default">Cancel</button>
      </div>
    </div>

    <div id="id_save_as_dialog" class="pa_hidden">
      <form class="form-inline">
        <div class="form-group">
          <label for="id_save_as_path">Please enter a path:</label>
          <input id="id_save_as_path" class="form-control" style="width: 100%;" />
        </div>
        <img id="id_save_as_spinner" class="spinner pa_hidden" src="/static/anywhere/images/spinner-small.gif" />
        <p>
          <span id="id_save_as_error" class="error_message"></span>
        </p>
        <div class="dialog_buttons">
          <button id="id_save_as_ok" type="submit" class="btn btn-primary">Save</button>
          <button id="id_save_as_cancel" type="button" class="btn btn-default">Cancel</button>
        </div>
      </form>
    </div>

    <div class="modal fade" id="id_file_sharing_modal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
            <h4 class="modal-title" id="myModalLabel">File Sharing options</h4>
          </div>
          <div class="modal-body">
            <div id="id_file_sharing_options"></div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>

  </div>


        
      </div>

        


        <div id="id_feedback_dialog" title="Help us improve" style="display:none">
    <div id="id_feedback_dialog_blurb_big" class="dialog_blurb_big">
        It's always a pleasure to hear from you!
    </div>
    <div id="id_feedback_dialog_blurb_small">
        Ask us a question, or tell us what you love or hate about PythonAnywhere.<br/>
        We'll get back to you over email ASAP.
    </div>
    <textarea id="id_feedback_dialog_text" rows="6"></textarea>
    <input id="id_feedback_dialog_email_address" type="text" placeholder="Email address (optional - only necessary if you would like us to contact you)"/>
    
    <div id="id_feedback_dialog_error" style="display: none">
        Sorry, there was an error connecting to the server. <br/>Please try again in a few moments...
    </div>
    <div id="id_feedback_dialog_rate_limit_error" style="display: none">
        Sorry, we have had to rate-limit your feedback sending.<br/>Please try again in a few moments...
    </div>
    <div id="id_feedback_dialog_success" style="display: none">
        Thanks for the feedback! Our tireless devs will get back to you soon.
    </div>
    <div class="dialog_buttons">
        <img id="id_feedback_dialog_spinner" src="/static/anywhere/images/spinner-small.gif" />
        <button class="btn btn-primary" id="id_feedback_dialog_ok_button">OK</button>
        <button class="btn btn-default" id="id_feedback_dialog_cancel_button">Cancel</button>
    </div>
    <div id="id_feedback_dialog_only_close_button" style="display: none">
        <button class="btn btn-primary" id="id_feedback_dialog_close_button">Close</button>
    </div>
</div>


        
            <script>
                (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
                (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
                m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
                })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

                ga('create', 'UA-18014859-6', 'auto');
                ga('send', 'pageview');
            </script>
        

        
        <!-- preload font awesome fonts to avoid glitch when switching icons -->
        <div style="width: 0; height: 0; overflow: hidden"><i class="fa fa-square-o fa-3x" ></i></div>
    </body>
</html>
