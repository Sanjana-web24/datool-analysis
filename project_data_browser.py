
# import os
# import re
# import shutil
# from flask import Flask, request, redirect, url_for, render_template_string, abort, send_from_directory, flash

# DATA_DIR = "data"
# ALLOWED_EXTENSIONS = {'xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt', 'zip'}

# app = Flask(__name__)
# app.secret_key = "supersecretkey"
# app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200 MB max upload size

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def sanitize_name(name):
#     # Allow uppercase letters, digits, dot, comma, underscore, hyphen, spaces converted to underscore
#     name = name.strip()
#     name = name.replace(' ', '_')
#     # Remove any characters except these
#     name = re.sub(r'[^a-zA-Z0-9\.,_-]', '', name)
#     return name

# @app.route("/")
# def index():
#     if not os.path.exists(DATA_DIR):
#         os.mkdir(DATA_DIR)
#     projects = sorted([d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))])
#     return render_template_string("""
# <!DOCTYPE html>
# <html lang="en"><head>
# <meta charset="UTF-8" />
# <meta name="viewport" content="width=device-width, initial-scale=1" />
# <title>Project Excel Browser</title>
# <style>
#   body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background:#f4f7fa; padding:1em; color:#222; }
#   h1 { color: #1a73e8; }
#   ul { padding-left: 1.2em; }
#   li { margin-bottom: 0.4em; position: relative; }
#   a.project-link { color: #1a73e8; text-decoration:none; cursor:pointer; }
#   a.project-link:hover { text-decoration: underline; }
#   form { margin-top: 2em; }
#   input[type=text] { padding: 0.4em; font-size: 1em; width: 250px; }
#   input[type=submit] { background: #1a73e8; color:white; padding: 0.5em 1em; border:none; border-radius:4px; cursor:pointer; }
#   input[type=submit]:hover { background: #155ab6; }
#   .flash-message { background-color: #D4EDDA; color: #155724; padding: 10px; border-radius: 4px; margin-bottom: 1em; border: 1px solid #C3E6CB; }
#   /* Context menu styles */
#   .context-menu {
#     position: absolute;
#     z-index: 1000;
#     width: 120px;
#     background: white;
#     box-shadow: 0 2px 8px rgba(0,0,0,0.15);
#     border-radius: 4px;
#     display: none;
#   }
#   .context-menu ul {
#     list-style: none;
#     margin: 4px 0;
#     padding: 0;
#   }
#   .context-menu li {
#     padding: 8px 12px;
#     cursor: pointer;
#   }
#   .context-menu li:hover {
#     background-color: #1a73e8;
#     color: white;
#   }
# </style>
# </head><body>
# <h1>Project Excel Browser</h1>

# {% with messages = get_flashed_messages() %}
#   {% if messages %}
#     <div class="flash-message">
#     {% for message in messages %}
#       <p>{{ message }}</p>
#     {% endfor %}
#     </div>
#   {% endif %}
# {% endwith %}

# <h2>Projects</h2>
# <ul id="project-list">
#   {% if projects %}
#     {% for proj in projects %}
#       <li data-project="{{ proj }}">
#         <a href="{{ url_for('project_overview', project_name=proj) }}" class="project-link">{{ proj }}</a>
#       </li>
#     {% endfor %}
#   {% else %}
#     <li>No projects created yet.</li>
#   {% endif %}
# </ul>

# <form action="{{ url_for('create_project') }}" method="post">
#   <label for="project_name">Create New Project:</label><br />
#   <input id="project_name" name="project_name" type="text" placeholder="Enter project name" required />
#   <input type="submit" value="Create Project" />
# </form>

# <!-- Hidden forms for rename/delete -->
# <form id="rename-project-form" action="" method="post" style="display:none;">
#   <input type="text" name="new_name" id="rename-project-input" required />
# </form>
# <form id="delete-project-form" action="" method="post" style="display:none;"></form>

# <!-- Context Menu -->
# <div id="context-menu" class="context-menu">
#   <ul>
#     <li id="rename-option">Rename</li>
#     <li id="delete-option">Delete</li>
#   </ul>
# </div>

# <script>
#   const contextMenu = document.getElementById('context-menu');
#   let currentTarget = null;
#   const renameForm = document.getElementById('rename-project-form');
#   const renameInput = document.getElementById('rename-project-input');
#   const deleteForm = document.getElementById('delete-project-form');

#   document.addEventListener('click', () => {
#     contextMenu.style.display = 'none';
#     currentTarget = null;
#   });

#   document.getElementById('project-list').addEventListener('contextmenu', function(e) {
#     e.preventDefault();
#     let target = e.target;
#     while (target && !target.dataset.project) {
#       target = target.parentElement;
#     }
#     if (!target) return;
#     currentTarget = target;
#     const projName = currentTarget.dataset.project;

#     contextMenu.style.top = e.pageY + "px";
#     contextMenu.style.left = e.pageX + "px";
#     contextMenu.style.display = 'block';
#   });

#   document.getElementById('rename-option').addEventListener('click', function(){
#     if(!currentTarget) return;
#     const projName = currentTarget.dataset.project;
#     renameInput.value = projName;
#     renameForm.action = `/rename_project/${encodeURIComponent(projName)}`;
#     renameForm.style.display = 'block';
#     renameInput.focus();
#     contextMenu.style.display = 'none';
#   });

#   renameForm.addEventListener('submit', function(e){
#     e.preventDefault();
#     if(!renameInput.value.trim()) {
#       alert("New name cannot be empty");
#       return;
#     }
#     renameForm.submit();
#   });

#   document.getElementById('delete-option').addEventListener('click', function(){
#     if(!currentTarget) return;
#     const projName = currentTarget.dataset.project;
#     if(confirm(`Are you sure you want to delete the project '${projName}'? This action cannot be undone.`)){
#       deleteForm.action = `/delete_project/${encodeURIComponent(projName)}`;
#       deleteForm.method = 'post';
#       deleteForm.submit();
#     }
#     contextMenu.style.display = 'none';
#   });
# </script>
# </body></html>
# """, projects=projects)


# @app.route("/create_project", methods=["POST"])
# def create_project():
#     name = request.form.get("project_name", "")
#     safe_name = sanitize_name(name)
#     if not safe_name:
#         flash("Invalid project name. Please try again.")
#         return redirect(url_for("index"))
#     proj_path = os.path.join(DATA_DIR, safe_name)
#     if not os.path.exists(proj_path):
#         os.makedirs(proj_path)
#         flash(f"Project '{safe_name}' created successfully.")
#     else:
#         flash(f"Project '{safe_name}' already exists.")
#     return redirect(url_for("project_overview", project_name=safe_name))


# @app.route("/rename_project/<old_name>", methods=["POST"])
# def rename_project(old_name):
#     new_name = request.form.get("new_name", "")
#     old_safe = old_name
#     new_safe = sanitize_name(new_name)
#     if not new_safe:
#         flash("Invalid new project name.")
#         return redirect(url_for("index"))

#     old_path = os.path.join(DATA_DIR, old_safe)
#     new_path = os.path.join(DATA_DIR, new_safe)

#     if not os.path.isdir(old_path):
#         flash("Original project does not exist.")
#         return redirect(url_for("index"))
#     if os.path.exists(new_path):
#         flash("Target project name already exists.")
#         return redirect(url_for("index"))

#     os.rename(old_path, new_path)
#     flash(f"Project renamed '{old_safe}' → '{new_safe}'.")
#     return redirect(url_for("index"))


# @app.route("/delete_project/<project_name>", methods=["POST"])
# def delete_project(project_name):
#     proj_path = os.path.join(DATA_DIR, project_name)
#     if not os.path.isdir(proj_path):
#         flash("Project does not exist.")
#         return redirect(url_for("index"))
#     try:
#         shutil.rmtree(proj_path)
#         flash(f"Project '{project_name}' deleted successfully.")
#     except Exception as e:
#         flash(f"Error deleting project: {e}")
#     return redirect(url_for("index"))


# @app.route("/project/<project_name>")
# def project_overview(project_name):
#     proj_path = os.path.join(DATA_DIR, project_name)
#     if not os.path.isdir(proj_path):
#         abort(404, description="Project not found")

#     ip_modules = sorted([d for d in os.listdir(proj_path) if os.path.isdir(os.path.join(proj_path, d))])
#     return render_template_string("""
# <!DOCTYPE html>
# <html lang="en"><head>
# <meta charset="UTF-8" />
# <meta name="viewport" content="width=device-width, initial-scale=1" />
# <title>Project: {{ project_name }}</title>
# <style>
#   body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background:#fff; margin:1em; color:#222; }
#   h1 { color: #1a73e8;}
#   ul { padding-left: 1.2em; list-style:none; }
#   li { margin-bottom: 0.6em; position: relative; }
#   a.ip-module-link { color: #1a73e8; text-decoration:none; cursor:pointer; }
#   a.ip-module-link:hover { text-decoration: underline; }
#   form { margin-top: 2em; }
#   input[type=text] { padding:0.4em; font-size:1em; }
#   input[type=submit], button { background: #1a73e8; color:white; border:none; border-radius:4px; cursor:pointer; padding: 0.3em 0.6em; }
#   input[type=submit]:hover, button:hover { background: #155ab6; }
#   /* Context menu styles */
#   .context-menu {
#     position: absolute;
#     z-index: 1000;
#     width: 120px;
#     background: white;
#     box-shadow: 0 2px 8px rgba(0,0,0,0.15);
#     border-radius: 4px;
#     display: none;
#   }
#   .context-menu ul { list-style: none; margin: 4px 0; padding: 0; }
#   .context-menu li { padding: 8px 12px; cursor: pointer;}
#   .context-menu li:hover { background-color: #1a73e8; color: white; }
#   .flash-message { background-color: #D4EDDA; color: #155724; padding: 10px; border-radius: 4px; margin-bottom: 1em; border: 1px solid #C3E6CB; }
# </style>
# </head><body>
# <h1>Project: {{ project_name }}</h1>

# {% with messages = get_flashed_messages() %}
#   {% if messages %}
#     <div class="flash-message">
#     {% for message in messages %}
#       <p>{{ message }}</p>
#     {% endfor %}
#     </div>
#   {% endif %}
# {% endwith %}

# <h2>IP / Module Names</h2>
# <ul id="ip-module-list">
# {% if ip_modules %}
#   {% for ip in ip_modules %}
#     <li data-ip="{{ ip }}">
#       <a href="{{ url_for('ip_module_overview', project_name=project_name, ip_module_name=ip) }}" class="ip-module-link">{{ ip }}</a>
#     </li>
#   {% endfor %}
# {% else %}
#   <li>No IP / Module added yet.</li>
# {% endif %}
# </ul>

# <form action="{{ url_for('add_ip_module', project_name=project_name) }}" method="post" style="margin-top:2em;">
#   <label for="ip_module_name">Add new IP / Module:</label><br />
#   <input id="ip_module_name" name="ip_module_name" type="text" placeholder="Enter IP or module name" required />
#   <input type="submit" value="Add IP / Module" />
# </form>

# <p><a href="{{ url_for('index') }}">Back to Projects</a></p>

# <!-- Hidden forms for rename/delete -->
# <form id="rename-ip-form" action="" method="post" style="display:none;">
#   <input type="text" name="new_name" id="rename-ip-input" required />
# </form>
# <form id="delete-ip-form" action="" method="post" style="display:none;"></form>

# <!-- Context Menu -->
# <div id="context-menu" class="context-menu">
#   <ul>
#     <li id="rename-option">Rename</li>
#     <li id="delete-option">Delete</li>
#   </ul>
# </div>

# <script>
#   const contextMenu = document.getElementById('context-menu');
#   let currentTarget = null;
#   const renameForm = document.getElementById('rename-ip-form');
#   const renameInput = document.getElementById('rename-ip-input');
#   const deleteForm = document.getElementById('delete-ip-form');

#   document.addEventListener('click', () => {
#     contextMenu.style.display = 'none';
#     currentTarget = null;
#   });

#   document.getElementById('ip-module-list').addEventListener('contextmenu', function(e) {
#     e.preventDefault();
#     let target = e.target;
#     while (target && !target.dataset.ip) {
#       target = target.parentElement;
#     }
#     if (!target) return;
#     currentTarget = target;
#     const ipName = currentTarget.dataset.ip;

#     contextMenu.style.top = e.pageY + "px";
#     contextMenu.style.left = e.pageX + "px";
#     contextMenu.style.display = 'block';
#   });

#   document.getElementById('rename-option').addEventListener('click', function(){
#     if(!currentTarget) return;
#     const ipName = currentTarget.dataset.ip;
#     renameInput.value = ipName;
#     renameForm.action = `/project/{{ project_name }}/rename_ip_module/${encodeURIComponent(ipName)}`;
#     renameForm.style.display = 'block';
#     renameInput.focus();
#     contextMenu.style.display = 'none';
#   });

#   renameForm.addEventListener('submit', function(e){
#     e.preventDefault();
#     if(!renameInput.value.trim()) {
#       alert("New name cannot be empty");
#       return;
#     }
#     renameForm.submit();
#   });

#   document.getElementById('delete-option').addEventListener('click', function(){
#     if(!currentTarget) return;
#     const ipName = currentTarget.dataset.ip;
#     if(confirm(`Are you sure you want to delete the IP/Module '${ipName}'? This action cannot be undone.`)){
#       deleteForm.action = `/project/{{ project_name }}/delete_ip_module/${encodeURIComponent(ipName)}`;
#       deleteForm.method = 'post';
#       deleteForm.submit();
#     }
#     contextMenu.style.display = 'none';
#   });
# </script>
# </body></html>
# """, project_name=project_name, ip_modules=ip_modules)

# @app.route("/project/<project_name>/add_ip_module", methods=["POST"])
# def add_ip_module(project_name):
#     proj_path = os.path.join(DATA_DIR, project_name)
#     if not os.path.isdir(proj_path):
#         abort(404, "Project not found")

#     name = request.form.get("ip_module_name", "")
#     safe_name = sanitize_name(name)
#     if not safe_name:
#         flash("Invalid IP/Module name.")
#         return redirect(url_for("project_overview", project_name=project_name))

#     ip_path = os.path.join(proj_path, safe_name)
#     if not os.path.exists(ip_path):
#         os.makedirs(ip_path)

#     raw_path = os.path.join(ip_path, "Raw")
#     summary_path = os.path.join(ip_path, "Summary")
#     if not os.path.exists(raw_path):
#         os.makedirs(raw_path)
#     if not os.path.exists(summary_path):
#         os.makedirs(summary_path)

#     flash(f"IP/Module '{safe_name}' added successfully.")
#     return redirect(url_for("project_overview", project_name=project_name))

# @app.route("/project/<project_name>/rename_ip_module/<old_ip_module_name>", methods=["POST"])
# def rename_ip_module(project_name, old_ip_module_name):
#     proj_path = os.path.join(DATA_DIR, project_name)
#     old_path = os.path.join(proj_path, old_ip_module_name)
#     if not os.path.isdir(old_path):
#         flash(f"IP/Module '{old_ip_module_name}' does not exist.")
#         return redirect(url_for("project_overview", project_name=project_name))

#     new_name = request.form.get("new_name", "").strip()
#     new_safe_name = sanitize_name(new_name)
#     if not new_safe_name:
#         flash("Invalid new name for IP/Module.")
#         return redirect(url_for("project_overview", project_name=project_name))

#     new_path = os.path.join(proj_path, new_safe_name)
#     if os.path.exists(new_path):
#         flash(f"An IP/Module with the name '{new_safe_name}' already exists.")
#         return redirect(url_for("project_overview", project_name=project_name))

#     os.rename(old_path, new_path)
#     flash(f"IP/Module renamed '{old_ip_module_name}' → '{new_safe_name}'.")
#     return redirect(url_for("project_overview", project_name=project_name))

# @app.route("/project/<project_name>/delete_ip_module/<ip_module_name>", methods=["POST"])
# def delete_ip_module(project_name, ip_module_name):
#     proj_path = os.path.join(DATA_DIR, project_name)
#     target_path = os.path.join(proj_path, ip_module_name)
#     if not os.path.isdir(target_path):
#         flash(f"IP/Module '{ip_module_name}' does not exist.")
#         return redirect(url_for("project_overview", project_name=project_name))

#     try:
#         shutil.rmtree(target_path)
#         flash(f"IP/Module '{ip_module_name}' deleted successfully.")
#     except Exception as e:
#         flash(f"Error deleting IP/Module '{ip_module_name}': {e}")

#     return redirect(url_for("project_overview", project_name=project_name))

# def save_files_to_folder(files, folder):
#     saved = 0
#     for file in files:
#         if file and allowed_file(file.filename):
#             filename = file.filename
#             filename = re.sub(r'[^a-zA-Z0-9_.()-]', '_', filename)
#             file_path = os.path.join(folder, filename)
#             base, ext = os.path.splitext(filename)
#             counter = 1
#             while os.path.exists(file_path):
#                 filename = f"{base}({counter}){ext}"
#                 file_path = os.path.join(folder, filename)
#                 counter += 1
#             file.save(file_path)
#             saved += 1
#     return saved

# def list_files_in_folder(folder):
#     if not os.path.exists(folder):
#         return []
#     return sorted([f for f in os.listdir(folder) if allowed_file(f)])

# @app.route("/project/<project_name>/ip_module/<ip_module_name>")
# def ip_module_overview(project_name, ip_module_name):
#     return redirect(url_for("ip_module_summary", project_name=project_name, ip_module_name=ip_module_name))

# @app.route("/project/<project_name>/ip_module/<ip_module_name>/summary", methods=["GET", "POST"])
# def ip_module_summary(project_name, ip_module_name):
#     ip_path = os.path.join(DATA_DIR, project_name, ip_module_name, "Summary")
#     if not os.path.exists(ip_path):
#         abort(404, description="IP / Module or Summary folder not found")
#     if request.method == "POST":
#         files = request.files.getlist("files")
#         save_files_to_folder(files, ip_path)
#         return redirect(url_for("ip_module_summary", project_name=project_name, ip_module_name=ip_module_name))
#     files = list_files_in_folder(ip_path)
#     return render_template_string("""
# <!DOCTYPE html>
# <html lang="en"><head>
# <meta charset="UTF-8" />
# <meta name="viewport" content="width=device-width, initial-scale=1" />
# <title>Summary - {{ ip_module_name }} - {{ project_name }}</title>
# <style>
#   body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background:#fff; margin:1em; color:#222; }
#   h1 { color: #1a73e8; }
#   a { color: #1a73e8; text-decoration:none; margin-right: 1em; }
#   a:hover { text-decoration: underline; }
#   form { margin-top: 1em; margin-bottom: 2em; }
#   input[type=file] { margin-top: 0.4em; }
#   input[type=submit] { margin-top: 0.5em; background: #1a73e8; color: white; border: none; padding: 0.5em 1em; cursor: pointer; border-radius: 4px; }
#   input[type=submit]:hover { background: #155ab6; }
#   ul { padding-left: 1.2em; }
#   li { margin-bottom: 0.3em; }
# </style>
# </head><body>
# <h1>Project: {{ project_name }} / IP: {{ ip_module_name }} - Summary</h1>

# <p>
# <a href="{{ url_for('ip_module_summary', project_name=project_name, ip_module_name=ip_module_name) }}">Summary</a>
# <a href="{{ url_for('ip_module_raw', project_name=project_name, ip_module_name=ip_module_name) }}">Raw</a>
# <a href="{{ url_for('project_overview', project_name=project_name) }}">Projects</a>
# </p>

# <form action="{{ url_for('ip_module_summary', project_name=project_name, ip_module_name=ip_module_name) }}"
# method="post" enctype="multipart/form-data">
#   <label for="files">Upload Excel or ZIP files (multiple allowed):</label><br />
#   <input id="files" type="file" name="files" multiple
#          accept=".xls,.xlsx,.xlsm,.xlsb,.odf,.ods,.odt,.zip" required />
#   <br />
#   <input type="submit" value="Upload Files" />
# </form>

# <h3>Files</h3>
# {% if files %}
# <ul>
#   {% for f in files %}
#   <li><a href="{{ url_for('download_file', project_name=project_name,
#            ip_module_name=ip_module_name, folder='Summary', filename=f) }}">{{ f }}</a></li>
#   {% endfor %}
# </ul>
# {% else %}
# <p>No files uploaded yet.</p>
# {% endif %}
# </body></html>
# """, project_name=project_name, ip_module_name=ip_module_name, files=files)

# @app.route("/project/<project_name>/ip_module/<ip_module_name>/raw", methods=["GET", "POST"])
# def ip_module_raw(project_name, ip_module_name):
#     ip_path = os.path.join(DATA_DIR, project_name, ip_module_name, "Raw")
#     if not os.path.exists(ip_path):
#         abort(404, description="IP / Module or Raw folder not found")
#     if request.method == "POST":
#         files = request.files.getlist("files")
#         save_files_to_folder(files, ip_path)
#         return redirect(url_for("ip_module_raw", project_name=project_name, ip_module_name=ip_module_name))
#     files = list_files_in_folder(ip_path)
#     return render_template_string("""
# <!DOCTYPE html>
# <html lang="en"><head>
# <meta charset="UTF-8" />
# <meta name="viewport" content="width=device-width, initial-scale=1" />
# <title>Raw - {{ ip_module_name }} - {{ project_name }}</title>
# <style>
#   body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background:#fff; margin:1em; color:#222; }
#   h1 { color: #1a73e8; }
#   a { color: #1a73e8; text-decoration:none; margin-right: 1em; }
#   a:hover { text-decoration: underline; }
#   form { margin-top: 1em; margin-bottom: 2em; }
#   input[type=file] { margin-top: 0.4em; }
#   input[type=submit] { margin-top: 0.5em; background: #1a73e8; color: white; border: none; padding: 0.5em 1em; cursor: pointer; border-radius: 4px; }
#   input[type=submit]:hover { background: #155ab6; }
#   ul { padding-left: 1.2em; }
#   li { margin-bottom: 0.3em; }
# </style>
# </head><body>
# <h1>Project: {{ project_name }} / IP: {{ ip_module_name }} - Raw</h1>

# <p>
# <a href="{{ url_for('ip_module_summary', project_name=project_name, ip_module_name=ip_module_name) }}">
# Summary</a>
# <a href="{{ url_for('ip_module_raw', project_name=project_name, ip_module_name=ip_module_name) }}">
# Raw</a>
# <a href="{{ url_for('project_overview', project_name=project_name) }}">Projects</a>
# </p>

# <form action="{{ url_for('ip_module_raw', project_name=project_name, ip_module_name=ip_module_name) }}"
# method="post" enctype="multipart/form-data">
#   <label for="files">Upload Excel or ZIP files (multiple allowed):</label><br />
#   <input id="files" type="file" name="files" multiple
#          accept=".xls,.xlsx,.xlsm,.xlsb,.odf,.ods,.odt,.zip" required />
#   <br />
#   <input type="submit" value="Upload Files" />
# </form>

# <h3>Files</h3>
# {% if files %}
# <ul>
#   {% for f in files %}
#   <li><a href="{{ url_for('download_file', project_name=project_name,
#            ip_module_name=ip_module_name, folder='Raw', filename=f) }}">{{ f }}</a></li>
#   {% endfor %}
# </ul>
# {% else %}
# <p>No files uploaded yet.</p>
# {% endif %}
# </body></html>
# """, project_name=project_name, ip_module_name=ip_module_name, files=files)

# @app.route("/project/<project_name>/ip_module/<ip_module_name>/<folder>/files/<path:filename>")
# def download_file(project_name, ip_module_name, folder, filename):
#     folder = folder.capitalize()
#     if folder not in {"Raw", "Summary"}:
#         abort(404)
#     dirpath = os.path.join(DATA_DIR, project_name, ip_module_name, folder)
#     if not os.path.isdir(dirpath):
#         abort(404)
#     filename = os.path.basename(filename)
#     filepath = os.path.join(dirpath, filename)
#     if not os.path.isfile(filepath):
#         abort(404)
#     return send_from_directory(dirpath, filename, as_attachment=True)


# if __name__ == "__main__":
#     if not os.path.exists(DATA_DIR):
#         os.mkdir(DATA_DIR)
#     app.run(host="127.0.0.1", port=5000, debug=True)















# import os
# import re
# import shutil
# from flask import Flask, request, redirect, url_for, render_template_string, abort, send_from_directory, flash, jsonify

# DATA_DIR = "data"
# ALLOWED_EXTENSIONS = {'xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt', 'zip'}

# app = Flask(__name__)
# app.secret_key = "supersecretkey"
# app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200 MB max upload size

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def sanitize_name(name):
#     name = name.strip()
#     name = name.replace(' ', '_')
#     name = re.sub(r'[^a-zA-Z0-9\.,_-]', '', name)
#     return name

# @app.route("/")
# def index():
#     if not os.path.exists(DATA_DIR):
#         os.mkdir(DATA_DIR)
#     projects = sorted([d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))])
#     return render_template_string("""
# <!DOCTYPE html>
# <html lang="en"><head>
# <meta charset="UTF-8" />
# <meta name="viewport" content="width=device-width, initial-scale=1" />
# <title>Project Excel Browser</title>
# <style>
#   body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background:#f4f7fa; padding:1em; color:#222; }
#   h1 { color: #1a73e8; }
#   ul { padding-left: 1.2em; }
#   li { margin-bottom: 0.4em; position: relative; }
#   a.project-link { color: #1a73e8; text-decoration:none; cursor:pointer; }
#   a.project-link:hover { text-decoration: underline; }
#   form { margin-top: 2em; }
#   input[type=text] { padding: 0.4em; font-size: 1em; width: 250px; }
#   input[type=submit] { background: #1a73e8; color:white; padding: 0.5em 1em; border:none; border-radius:4px; cursor:pointer; }
#   input[type=submit]:hover { background: #155ab6; }
#   .flash-message { background-color: #D4EDDA; color: #155724; padding: 10px; border-radius: 4px; margin-bottom: 1em; border: 1px solid #C3E6CB; }
# </style>
# </head><body>
# <h1>Project Excel Browser</h1>

# {% with messages = get_flashed_messages() %}
#   {% if messages %}
#     <div class="flash-message">
#     {% for message in messages %}
#       <p>{{ message }}</p>
#     {% endfor %}
#     </div>
#   {% endif %}
# {% endwith %}

# <h2>Projects</h2>
# <ul id="project-list">
#   {% if projects %}
#     {% for proj in projects %}
#       <li data-project="{{ proj }}">
#         <a href="{{ url_for('project_overview', project_name=proj) }}" class="project-link">{{ proj }}</a>
#       </li>
#     {% endfor %}
#   {% else %}
#     <li>No projects created yet.</li>
#   {% endif %}
# </ul>

# <form action="{{ url_for('create_project') }}" method="post">
#   <label for="project_name">Create New Project:</label><br />
#   <input id="project_name" name="project_name" type="text" placeholder="Enter project name" required />
#   <input type="submit" value="Create Project" />
# </form>

# </body></html>
# """, projects=projects)

# @app.route("/create_project", methods=["POST"])
# def create_project():
#     name = request.form.get("project_name", "")
#     safe_name = sanitize_name(name)
#     if not safe_name:
#         flash("Invalid project name. Please try again.")
#         return redirect(url_for("index"))
#     proj_path = os.path.join(DATA_DIR, safe_name)
#     if not os.path.exists(proj_path):
#         os.makedirs(proj_path)
#         flash(f"Project '{safe_name}' created successfully.")
#     else:
#         flash(f"Project '{safe_name}' already exists.")
#     return redirect(url_for("project_overview", project_name=safe_name))

# @app.route("/project/<project_name>")
# def project_overview(project_name):
#     proj_path = os.path.join(DATA_DIR, project_name)
#     if not os.path.isdir(proj_path):
#         abort(404, description="Project not found")
#     ip_modules = sorted([d for d in os.listdir(proj_path) if os.path.isdir(os.path.join(proj_path, d))])
#     return render_template_string("""
# <!DOCTYPE html>
# <html lang="en"><head>
# <meta charset="UTF-8" />
# <meta name="viewport" content="width=device-width, initial-scale=1" />
# <title>Project: {{ project_name }}</title>
# <style>
#   body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background:#fff; margin:1em; color:#222; }
#   h1 { color: #1a73e8;}
#   ul { padding-left: 1.2em; list-style:none; }
#   li { margin-bottom: 0.6em; position: relative; }
#   a.ip-module-link { color: #1a73e8; text-decoration:none; cursor:pointer; }
#   a.ip-module-link:hover { text-decoration: underline; }
#   form { margin-top: 2em; }
#   input[type=text] { padding:0.4em; font-size:1em; }
#   input[type=submit], button { background: #1a73e8; color:white; border:none; border-radius:4px; cursor:pointer; padding: 0.3em 0.6em; }
#   input[type=submit]:hover, button:hover { background: #155ab6; }
#   .flash-message { background-color: #D4EDDA; color: #155724; padding: 10px; border-radius: 4px; margin-bottom: 1em; border: 1px solid #C3E6CB; }
# </style>
# </head><body>
# <h1>Project: {{ project_name }}</h1>

# {% with messages = get_flashed_messages() %}
#   {% if messages %}
#     <div class="flash-message">
#     {% for message in messages %}
#       <p>{{ message }}</p>
#     {% endfor %}
#     </div>
#   {% endif %}
# {% endwith %}

# <h2>IP / Module Names</h2>
# <ul id="ip-module-list">
# {% if ip_modules %}
#   {% for ip in ip_modules %}
#     <li data-ip="{{ ip }}">
#       <a href="{{ url_for('ip_module_overview', project_name=project_name, ip_module_name=ip) }}" class="ip-module-link">{{ ip }}</a>
#     </li>
#   {% endfor %}
# {% else %}
#   <li>No IP / Module added yet.</li>
# {% endif %}
# </ul>

# <form action="{{ url_for('add_ip_module', project_name=project_name) }}" method="post" style="margin-top:2em;">
#   <label for="ip_module_name">Add new IP / Module:</label><br />
#   <input id="ip_module_name" name="ip_module_name" type="text" placeholder="Enter IP or module name" required />
#   <input type="submit" value="Add IP / Module" />
# </form>

# <p><a href="{{ url_for('index') }}">Back to Projects</a></p>

# </body></html>
# """, project_name=project_name, ip_modules=ip_modules)

# @app.route("/project/<project_name>/add_ip_module", methods=["POST"])
# def add_ip_module(project_name):
#     proj_path = os.path.join(DATA_DIR, project_name)
#     if not os.path.isdir(proj_path):
#         abort(404, "Project not found")
#     name = request.form.get("ip_module_name", "")
#     safe_name = sanitize_name(name)
#     if not safe_name:
#         flash("Invalid IP/Module name.")
#         return redirect(url_for("project_overview", project_name=project_name))
#     ip_path = os.path.join(proj_path, safe_name)
#     if not os.path.exists(ip_path):
#         os.makedirs(ip_path)
#     raw_path = os.path.join(ip_path, "Raw")
#     summary_path = os.path.join(ip_path, "Summary")
#     if not os.path.exists(raw_path):
#         os.makedirs(raw_path)
#     if not os.path.exists(summary_path):
#         os.makedirs(summary_path)
#     flash(f"IP/Module '{safe_name}' added successfully.")
#     return redirect(url_for("project_overview", project_name=project_name))

# @app.route("/project/<project_name>/ip_module/<ip_module_name>")
# def ip_module_overview(project_name, ip_module_name):
#     # Redirecting to summary by default
#     return redirect(url_for("ip_module_summary", project_name=project_name, ip_module_name=ip_module_name))

# def save_files_to_folder(files, folder):
#     saved = 0
#     for file in files:
#         if file and allowed_file(file.filename):
#             filename = file.filename
#             filename = re.sub(r'[^a-zA-Z0-9_.()-]', '_', filename)
#             file_path = os.path.join(folder, filename)
#             base, ext = os.path.splitext(filename)
#             counter = 1
#             while os.path.exists(file_path):
#                 filename = f"{base}({counter}){ext}"
#                 file_path = os.path.join(folder, filename)
#                 counter += 1
#             file.save(file_path)
#             saved += 1
#     return saved

# def list_files_in_folder(folder):
#     if not os.path.exists(folder):
#         return []
#     return sorted([f for f in os.listdir(folder) if allowed_file(f)])

# @app.route("/project/<project_name>/ip_module/<ip_module_name>/summary", methods=["GET", "POST"])
# def ip_module_summary(project_name, ip_module_name):
#     ip_path = os.path.join(DATA_DIR, project_name, ip_module_name, "Summary")
#     if not os.path.exists(ip_path):
#         abort(404, description="IP / Module or Summary folder not found")
#     if request.method == "POST":
#         files = request.files.getlist("files")
#         save_files_to_folder(files, ip_path)
#         return redirect(url_for("ip_module_summary", project_name=project_name, ip_module_name=ip_module_name))
#     files = list_files_in_folder(ip_path)
#     return render_template_string("""
# <!DOCTYPE html>
# <html lang="en"><head>
# <meta charset="UTF-8" />
# <meta name="viewport" content="width=device-width, initial-scale=1" />
# <title>Summary - {{ ip_module_name }} - {{ project_name }}</title>
# <style>
#   body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background:#fff; margin:1em; color:#222; }
#   h1 { color: #1a73e8; }
#   a { color: #1a73e8; text-decoration:none; margin-right: 1em; }
#   a:hover { text-decoration: underline; }
#   form { margin-top: 1em; margin-bottom: 2em; }
#   input[type=file] { margin-top: 0.4em; }
#   input[type=submit] { margin-top: 0.5em; background: #1a73e8; color: white; border: none; padding: 0.5em 1em; cursor: pointer; border-radius: 4px; }
#   input[type=submit]:hover { background: #155ab6; }
#   ul { padding-left: 1.2em; }
#   li { margin-bottom: 0.3em; }
# </style>
# </head><body>
# <h1>Project: {{ project_name }} / IP: {{ ip_module_name }} - Summary</h1>

# <p>
# <a href="{{ url_for('ip_module_summary', project_name=project_name, ip_module_name=ip_module_name) }}">Summary</a>
# <a href="{{ url_for('ip_module_raw', project_name=project_name, ip_module_name=ip_module_name) }}">Raw</a>
# <a href="{{ url_for('project_overview', project_name=project_name) }}">Projects</a>
# </p>

# <form action="{{ url_for('ip_module_summary', project_name=project_name, ip_module_name=ip_module_name) }}"
# method="post" enctype="multipart/form-data">
#   <label for="files">Upload Excel or ZIP files (multiple allowed):</label><br />
#   <input id="files" type="file" name="files" multiple
#          accept=".xls,.xlsx,.xlsm,.xlsb,.odf,.ods,.odt,.zip" required />
#   <br />
#   <input type="submit" value="Upload Files" />
# </form>

# <h3>Files</h3>
# {% if files %}
# <ul>
#   {% for f in files %}
#   <li><a href="{{ url_for('download_file', project_name=project_name,
#            ip_module_name=ip_module_name, folder='Summary', filename=f) }}">{{ f }}</a></li>
#   {% endfor %}
# </ul>
# {% else %}
# <p>No files uploaded yet.</p>
# {% endif %}
# </body></html>
# """, project_name=project_name, ip_module_name=ip_module_name, files=files)

# @app.route("/project/<project_name>/ip_module/<ip_module_name>/raw", methods=["GET", "POST"])
# def ip_module_raw(project_name, ip_module_name):
#     ip_path = os.path.join(DATA_DIR, project_name, ip_module_name, "Raw")
#     if not os.path.exists(ip_path):
#         abort(404, description="IP / Module or Raw folder not found")
#     if request.method == "POST":
#         files = request.files.getlist("files")
#         save_files_to_folder(files, ip_path)
#         return redirect(url_for("ip_module_raw", project_name=project_name, ip_module_name=ip_module_name))
#     files = list_files_in_folder(ip_path)
#     return render_template_string("""
# <!DOCTYPE html>
# <html lang="en"><head>
# <meta charset="UTF-8" />
# <meta name="viewport" content="width=device-width, initial-scale=1" />
# <title>Raw - {{ ip_module_name }} - {{ project_name }}</title>
# <style>
#   body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background:#fff; margin:1em; color:#222; }
#   h1 { color: #1a73e8; }
#   a { color: #1a73e8; text-decoration:none; margin-right: 1em; }
#   a:hover { text-decoration: underline; }
#   form { margin-top: 1em; margin-bottom: 2em; }
#   input[type=file] { margin-top: 0.4em; }
#   input[type=submit] { margin-top: 0.5em; background: #1a73e8; color: white; border: none; padding: 0.5em 1em; cursor: pointer; border-radius: 4px; }
#   input[type=submit]:hover { background: #155ab6; }
#   ul { padding-left: 1.2em; }
#   li { margin-bottom: 0.3em; }
# </style>
# </head><body>
# <h1>Project: {{ project_name }} / IP: {{ ip_module_name }} - Raw</h1>

# <p>
# <a href="{{ url_for('ip_module_summary', project_name=project_name, ip_module_name=ip_module_name) }}">
# Summary</a>
# <a href="{{ url_for('ip_module_raw', project_name=project_name, ip_module_name=ip_module_name) }}">
# Raw</a>
# <a href="{{ url_for('project_overview', project_name=project_name) }}">Projects</a>
# </p>

# <form action="{{ url_for('ip_module_raw', project_name=project_name, ip_module_name=ip_module_name) }}"
# method="post" enctype="multipart/form-data">
#   <label for="files">Upload Excel or ZIP files (multiple allowed):</label><br />
#   <input id="files" type="file" name="files" multiple
#          accept=".xls,.xlsx,.xlsm,.xlsb,.odf,.ods,.odt,.zip" required />
#   <br />
#   <input type="submit" value="Upload Files" />
# </form>

# <h3>Files</h3>
# {% if files %}
# <ul>
#   {% for f in files %}
#   <li><a href="{{ url_for('download_file', project_name=project_name,
#            ip_module_name=ip_module_name, folder='Raw', filename=f) }}">{{ f }}</a></li>
#   {% endfor %}
# </ul>
# {% else %}
# <p>No files uploaded yet.</p>
# {% endif %}
# </body></html>
# """, project_name=project_name, ip_module_name=ip_module_name, files=files)

# @app.route("/project/<project_name>/ip_module/<ip_module_name>/<folder>/files/<path:filename>")
# def download_file(project_name, ip_module_name, folder, filename):
#     folder = folder.capitalize()
#     if folder not in {"Raw", "Summary"}:
#         abort(404)
#     dirpath = os.path.join(DATA_DIR, project_name, ip_module_name, folder)
#     if not os.path.isdir(dirpath):
#         abort(404)
#     filename = os.path.basename(filename)
#     filepath = os.path.join(dirpath, filename)
#     if not os.path.isfile(filepath):
#         abort(404)
#     return send_from_directory(dirpath, filename, as_attachment=True)

# @app.route("/api/projects")
# def api_list_projects():
#     if not os.path.exists(DATA_DIR):
#         return jsonify([])
#     projects = sorted([d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))])
#     return jsonify(projects)

# @app.route("/api/project/<project_name>/ip_modules")
# def api_list_ip_modules(project_name):
#     proj_path = os.path.join(DATA_DIR, project_name)
#     if not os.path.isdir(proj_path):
#         return jsonify({"error": "Project not found"}), 404
#     ip_modules = sorted([d for d in os.listdir(proj_path) if os.path.isdir(os.path.join(proj_path, d))])
#     return jsonify(ip_modules)

# @app.route("/api/project/<project_name>/ip_module/<ip_module_name>/files/<folder>")
# def api_list_files(project_name, ip_module_name, folder):
#     folder = folder.capitalize()
#     if folder not in {"Raw", "Summary"}:
#         return jsonify({"error": "Invalid folder"}), 400
#     dirpath = os.path.join(DATA_DIR, project_name, ip_module_name, folder)
#     if not os.path.isdir(dirpath):
#         return jsonify({"error": "Folder not found"}), 404
#     files = list_files_in_folder(dirpath)
#     return jsonify(files)

# if __name__ == "__main__":
#     if not os.path.exists(DATA_DIR):
#         os.mkdir(DATA_DIR)
#     # Use host="0.0.0.0" to make it externally accessible if deployed properly
#     app.run(host="0.0.0.0", port=5000, debug=True)














