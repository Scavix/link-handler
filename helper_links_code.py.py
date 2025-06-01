import tkinter.messagebox as msg
import tkinter as tk
import os
import requests
from bs4 import BeautifulSoup

def main():
    root = tk.Tk()
    root.title("Basic Tkinter Program")
    root.geometry("700x350")
    root.configure(bg='lightblue')

    outstrings = []
    cachefiles = ["cachegen.tmp","cachecs.tmp","cachemath.tmp","cachecsutils.tmp"]
    for i in cachefiles:
        outstrings.append("")
    for cache in range(len(cachefiles)):
        try:
            if os.path.isfile(cachefiles[cache]):
                f = open(cachefiles[cache], "r")
                outstrings[cache] = f.read()
                f.close()
                os.remove(cachefiles[cache])
        except Exception as e:
            msg.showinfo("Error", e)

    input_frame = tk.Frame(root, bg='lightblue')
    input_frame.pack(pady=10)
    url_label = tk.Label(input_frame, text="Enter URL", bg='lightblue')
    url_label.pack(side=tk.LEFT)
    url_entry = tk.Entry(input_frame)
    url_entry.pack(side=tk.LEFT, padx=10)
    url_entry.insert(0, "Insert URL here")
    url_entry.bind("<FocusIn>", lambda e: url_entry.delete(0, tk.END) if url_entry.get() == "Insert URL here" else None)

    category_label = tk.Label(input_frame, text="Enter Category", bg='lightblue')
    category_label.pack(side=tk.LEFT)
    category_var = tk.StringVar(value="Generic")
    category_options = ["Generic", "Computer sciences", "Mathematics", "Computer utils"]
    category_menu = tk.OptionMenu(input_frame, category_var, *category_options)
    category_menu.config(bg='lightblue')
    category_menu.pack(side=tk.LEFT, padx=10)

    bold_var = tk.BooleanVar()
    bold_checkbox = tk.Checkbutton(input_frame, text="Bold", variable=bold_var, bg='lightblue')
    bold_checkbox.pack(side=tk.LEFT, padx=10)

    text_frame = tk.Frame(root, bg='lightblue')
    text_frame.pack(pady=5)

    # "Generic", "Computer sciences", "Mathematics", "Computer utils" text areas
    txt_generic = tk.Text(text_frame, height=3, width=80)
    txt_generic.pack(side=tk.TOP, pady=5)
    txt_cs = tk.Text(text_frame, height=3, width=80)
    txt_cs.pack(side=tk.TOP, pady=5)
    txt_math = tk.Text(text_frame, height=3, width=80)
    txt_math.pack(side=tk.TOP, pady=5)
    txt_utils = tk.Text(text_frame, height=3, width=80)
    txt_utils.pack(side=tk.TOP, pady=5)
    text_areas = [txt_generic, txt_cs, txt_math, txt_utils]
    for i, text_area in enumerate(text_areas):
        text_area.insert(tk.END, outstrings[i])

    button_frame = tk.Frame(root, bg='lightblue')
    button_frame.pack(pady=5)

    # "Add" "Generate Source" "Build Script" "Exit and Save" "Exit" buttons
    btn_add = tk.Button(button_frame, text="Add", command=lambda: add_url(url_entry.get(), category_var.get(), bold_var.get()))
    btn_add.pack(side=tk.LEFT, padx=5)
    btn_generate_source = tk.Button(button_frame, text="Generate Source", command=lambda: generate_source())
    btn_generate_source.pack(side=tk.LEFT, padx=5)
    btn_build_script = tk.Button(button_frame, text="Build Script", command=lambda: build_script())
    btn_build_script.pack(side=tk.LEFT, padx=5)
    btn_exit_save = tk.Button(button_frame, text="Exit and Save", command=lambda: exit_and_save())
    btn_exit_save.pack(side=tk.LEFT, padx=5)
    btn_exit = tk.Button(button_frame, text="Exit", command=lambda: just_quit())
    btn_exit.pack(side=tk.LEFT, padx=5)

    def add_url(url, category, bold):
        if url == "" or url == "Insert URL here":
            msg.showinfo("Error box", "Please enter a valid URL")
            return
        if category not in ["Generic", "Computer sciences", "Mathematics", "Computer utils"]:
            msg.showinfo("Error box", "Please select a valid category")
            return

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                if response.headers['Content-Type'].__contains__('application/pdf'):
                    title = url.split("/")[-1]
                elif not response.headers['Content-Type'].__contains__('text/html'):
                    msg.showinfo("Error box", "Web site is not HTML\n" + str(response.status_code))
                    return
                else:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    title = soup.title.string if soup.title else "No Title"
                #outstrings[category_options.index(category)] += "<li><a href = \"" + str(url).strip() + "\">" + ("<b>" if bold else "") + str(title) + ("</b>" if bold else "") + "</a></li>\n"
                outstrings[category_options.index(category)] = outstrings[category_options.index(category)].rstrip() + (("\n" if outstrings[category_options.index(category)] else "") + "<li><a href = \"" + str(url).strip() + "\">" + ("<b>" if bold else "") + str(title) + ("</b>" if bold else "") + "</a></li>")
                for i, text_area in enumerate(text_areas):
                    text_area.delete(1.0, tk.END)
                    text_area.insert(tk.END, outstrings[i])
            else:
                msg.showinfo("Error box", "Failed to fetch the URL" + str(response.status_code) + "\n" + response.reason + "\n" + response.text)
        except requests.RequestException as e:
            save_cache()
            msg.showinfo("Error box", f"Preventively saved. An error occurred: {e}")
    

    def generate_source():
        response = requests.get("https://raw.githubusercontent.com/Scavix/new-link-handler/main/helper_links_code.py")
        if response.status_code == 200:
            f = open("helper_links_code.py", "w")
            f.write(response.text)
            f.close()
            msg.showinfo("Confirmation box","Done generating source code")
        else:
            msg.showinfo("Error box","Web site does not exist or is not reachable")

    def build_script():
        response = requests.get("https://raw.githubusercontent.com/Scavix/new-link-handler/main/helper_links_build_script.bat")
        if response.status_code == 200:
            f = open("helper_links_build_script.bat", "w")
            f.write(response.text)
            f.close()
            msg.showinfo("Confirmation box","Done generating build script")
        else:
            msg.showinfo("Error box","Web site does not exist or is not reachable")

    def save_cache():
        for i, cache in enumerate(cachefiles):
            try:
                with open(cache, "w") as f:
                    f.write(outstrings[i])
            except Exception as e:
                msg.showinfo("Error", f"Failed to save cache {cache}: {e}")
        msg.showinfo("Cache Saved", "Cache saved.")

    def exit_and_save():
        save_cache() # if need
        root.quit()

    def just_quit():
        for cache in cachefiles:
            if os.path.isfile(cache):
                os.remove(cache)
        root.quit()

    root.mainloop()

if __name__ == "__main__":
    main()