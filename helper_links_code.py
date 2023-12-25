import requests
import PySimpleGUI as sg
from bs4 import BeautifulSoup
from datetime import datetime
import os.path

def main():
    outstrings = ["","",""]
    cachefiles = ["cachegen.tmp","cachecs.tmp","cachemath.tmp"]
    for cache in range(len(cachefiles)):
        try:
            if os.path.isfile(cachefiles[cache]):
                f = open(cachefiles[cache], "r")
                outstrings[cache] = f.read()
                f.close()
                os.remove(cachefiles[cache])
        except Exception as e:
            print(e)
            pass
    layout = [  [sg.Text('Enter URL'), sg.InputText(key='-URL-', default_text='Insert URL here'), sg.Text('Enter Category'), sg.Combo(values=('Generic', 'Computer sciences', 'Mathematics'), default_value='Generic', readonly=True, k='-COMBO-')],
                [sg.Multiline(expand_x=True, expand_y=True, key='-OUTPUTGEN-', default_text=outstrings[0])],
                [sg.Multiline(expand_x=True, expand_y=True, key='-OUTPUTCS-', default_text=outstrings[1])],
                [sg.Multiline(expand_x=True, expand_y=True, key='-OUTPUTMATH-', default_text=outstrings[2])],
                [sg.Button('Add'), sg.Button('Generate Source'), sg.Button('Build Script'), sg.Button('Exit and Save'), sg.Button('Exit')]]

    window = sg.Window('Url generate', layout, element_justification='c', finalize=True, size=(800, 300))

    try:
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Exit and Save':
                break
            if event == 'Exit':
                for cache in cachefiles:
                    if os.path.isfile(cache):
                        os.remove(cache)
                break
            elif event == 'Generate Source':
                response = requests.get("https://raw.githubusercontent.com/Scavix/link-handler/main/helper_links_code.py")
                if response.status_code == 200:
                    f = open("helper_links_code.py", "w")
                    f.write(response.text)
                    f.close()
                    sg.popup("Done")
                else:
                    sg.popup("Web site does not exist or is not reachable")
            elif event == 'Build Script':
                response = requests.get("https://raw.githubusercontent.com/Scavix/link-handler/main/helper_links_build_script.bat")
                if response.status_code == 200:
                    f = open("helper_links_build_script.bat", "w")
                    f.write(response.text)
                    f.close()
                    sg.popup("Done")
                else:
                    sg.popup("Web site does not exist or is not reachable")
            elif event == 'Add':
                url=window['-URL-'].get()
                category=window['-COMBO-'].get()
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
                }
                response = requests.get(values['-URL-'], headers=headers)
                if response.status_code == 200:
                    if response.headers['Content-Type'].__contains__('application/pdf'):
                        title = url.split('/')[-1]
                        outstrings[get_i_from_cat(category)] += "<li><a href = \"" + str(url).strip() + "\">" + str(title) + "</a></li>\n"
                    elif not response.headers['Content-Type'].__contains__('text/html'):
                        sg.popup("Web site is not HTML\n"+response.status_code)
                        continue
                    else:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        title = soup.title.string
                        outstrings[get_i_from_cat(category)] += "<li><a href = \"" + str(url).strip() + "\">" + str(title) + "</a></li>\n"
                        save_to(cachefiles[get_i_from_cat(category)],outstrings[get_i_from_cat(category)])
                else:
                    sg.popup("Web site does not exist or is not reachable\n"+response.status_code+"\n"+response.reason+"\n"+response.text)
            
                window['-OUTPUTGEN-'].update(value=outstrings[0])
                window['-OUTPUTCS-'].update(value=outstrings[1])
                window['-OUTPUTMATH-'].update(value=outstrings[2])
                window['-URL-'].update(value="")
    except:
        save_to(cachefiles[0],outstrings[0])    
        save_to(cachefiles[1],outstrings[1])
        save_to(cachefiles[2],outstrings[2])
        sg.popup("Found exception, cache saved")
    window.close()
    
def save_to(dir,myStr):
    f = open(dir, "w")
    f.write(myStr)
    f.close()

def get_i_from_cat(cat):
    if cat == "Generic":
        return 0
    elif cat == "Computer sciences":
        return 1
    elif cat == "Mathematics":
        return 2
    else:
        return 0

if __name__ == "__main__":
    main()
