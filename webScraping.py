from bs4 import BeautifulSoup
import urllib.request, json
import requests
import ssl
import certifi
# def WebScraping(link,site):
#     return {
#         'title' : 'Flask Course',
#         'instructor' : 'Mandar Patil',
#         'duration' : '12 hr',
#         'learner_count': '12421 total leaners',
#         'description': 'Start Learning Flask from complete start. We cover all the main topics in best way possible compared to all the available plaform till the date',
#         'comments' : ['Hello World','Great course']
#     }

def WebScraping(link, platform):
    site = platform
    c_url = link
    comments = []
    c = []

    result = {}
    if site == "Coursera":
        result['platform'] = 'Coursera'
        if '?' in c_url:
            c_url = c_url[:c_url.index("?")]
        url = c_url
        response = requests.get(url)
        htmlcontent = response.content
        soup = BeautifulSoup(htmlcontent, "html.parser")
        c = soup.findAll('h1', {'class': 'cds-119 cds-Typography-base css-1xy8ceb cds-121'})
        for i in c:
            result["title"] = i.text
        c = soup.findAll('div', {'class': 'content-inner'})
        for i in c:
            result["description"] = i.text
        c = soup.findAll('div', {'class': 'cds-119 cds-Typography-base css-h1jogs cds-121'})
        print(c)
        result["duration"] = c[1].text
        c = soup.findAll('span', {'class': 'cds-119 cds-Typography-base css-80vnnb cds-121'})

        result["instructor"] = c[0].text
        c = soup.findAll('div', {'class': 'cds-119 cds-Typography-base css-h1jogs cds-121'})
        print(c)

        result["learner_count"] = c[2].text
        result["learner_no"]= c[0].text
        res=[]

        url1 = url + "#reviews"
        response = requests.get(url1)
        htmlcontent = response.content
        soup = BeautifulSoup(htmlcontent, "html.parser")
        container = soup.findAll('div', {'class': 'css-l6lvqi'})

        # res.append(container.text)
            # for j in container:
            #     comments.append(j.text)
        # for j in container:
        #     comments.append(j.text)
        for item in container:
            res.append(item.text)

        result["comments"] =res
        print(result)

        return result

    elif site =="Youtube":
        result['v'] = link[link.index('=')+1:]
        videoId = c_url[(c_url.index("=") + 1):]
        print(videoId)
        url = 'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&id={}&key={}'.format(
            videoId, 'AIzaSyBmIvloIa6fEW-BwaSsDLJRwwH8lZvW5Os')
        response = urllib.request.urlopen(url,context=ssl.create_default_context(cafile=certifi.where()))
        data = response.read()
        data = json.loads(data)
        duration = data["items"][0]["contentDetails"]["duration"]
        result["duration"] = ''
        if duration.find('H')!=-1:
            result["duration"] = result["duration"] + (duration[duration.find('T') + 1:duration.find('H')] + ' Hr ')
        if duration.find('M')!=-1 and duration.find('H')!=-1:
            result["duration"] = result["duration"] + ' ' + (duration[duration.find('H') + 1:duration.find('M')] + ' Mins')
        elif duration.find('M')!=-1:
            result["duration"] = result["duration"] + ' ' +(duration[duration.find('T') + 1:duration.find('M')] + ' Mins')

        url = 'https://youtube.googleapis.com/youtube/v3/videos?part=statistics&id={}&key={}'.format(
            videoId, 'AIzaSyBmIvloIa6fEW-BwaSsDLJRwwH8lZvW5Os')
        response = urllib.request.urlopen(url,context=ssl.create_default_context(cafile=certifi.where()))
        data = response.read()
        data = json.loads(data)
        result["learner_count"] = data["items"][0]["statistics"]["viewCount"] + ' views'

        url = 'https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={}&key={}'.format(
            videoId, 'AIzaSyBmIvloIa6fEW-BwaSsDLJRwwH8lZvW5Os')
        response = urllib.request.urlopen(url,context=ssl.create_default_context(cafile=certifi.where()))
        data = response.read()
        data = json.loads(data)
        result["platform"] = "YouTube"
        result["title"] = data["items"][0]["snippet"]["title"]
        result["instructor"] = data["items"][0]["snippet"]["channelTitle"]
        result["description"] = data["items"][0]["snippet"]["description"]

        url = 'https://youtube.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&videoId={}&key={}'.format(
            videoId, 'AIzaSyBmIvloIa6fEW-BwaSsDLJRwwH8lZvW5Os')
        response = urllib.request.urlopen(url,context=ssl.create_default_context(cafile=certifi.where()))
        data = response.read()
        data = json.loads(data)
        for i in range(len(data["items"])):
            if data['items'][i]['snippet']['topLevelComment']['snippet']['textDisplay'] is not None:
                comments.append(data['items'][i]['snippet']['topLevelComment']['snippet']['textDisplay'])
        result["comments"] = comments
        return result

