import requests as a
import datetime as c
import multiprocessing

d = 14191261800  # Starting asset ID
e = 99999999999  # Ending asset ID
f = "https://economy.roproxy.com/v2/assets/{}/details"
g = set()
h = "https://discord.com/api/webhooks/1151459016648687676/7Kg1qAiZETFkxoClfVBeonJsLQnporVHKlCQr9PlhtrVhnrhAqiFCWtRnmJXUhRCw5rc"
i = ""
j = 0
k = c.datetime.now()
l = [
    "BIG Games Pets",
    "BIG Games™",
    "BIG Games Experimental",
    "BIG Games Super Fun",
    "CoderMitchell",
    "CoderJoey",
    "chickenputty",
    "CoderConner",
    "ForeverDev",
    "JamienChee",
    "BuildIntoGames",
    "",
    "",
    "",
    "",
    "",
    "",
]
m = {
    1: "Image",
    2: "T-Shirt",
    3: "Audio",
    4: "Mesh",
    5: "Lua",
    8: "Hat",
    9: "Place",
    10: "Model",
    13: "Decal",
    34: "Pass",
    37: "Code",
    39: "SolidModel",
    40: "MeshPart",
    80: "CodeSnippet"
}


def n(o, p):
    q = c.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    p["footer"] = {"text": f"Current Time: {q}"}
    r = {"embeds": [p]}
    s = {"Content-Type": "application/json"}
    t = a.post(o, json=r, headers=s)
    if t.status_code == 204:
        print("Sent Discord webhook")
    else:
        print(f"Failed to send Discord webhook: {t.text}")


def u(v):
    global j
    w = f.format(v)
    x = {"title": f"Asset ID: {v}", "color": 0xFF4500, "fields": []}
    try:
        y = a.get(w)
        if y.status_code == 200:
            z = y.json()
            aa = z.get("Name")
            ab = z.get("AssetTypeId")
            ac = z.get("Creator")
            if ac and ac.get("CreatorType") in ["User", "Group"]:
                ad = ac["Name"]
                if ad in l:
                    x["fields"].append({"name": "Asset Name", "value": aa})
                    x["fields"].append({"name": "Asset ID", "value": str(v)})
                    x["fields"].append({"name": "Asset Type", "value": m.get(ab, "Unknown")})
                    x["fields"].append({"name": "Creator Name", "value": ad})
                    x["fields"].append({"name": "Creator Type", "value": ac["CreatorType"]})
                    ae = f"https://www.roblox.com/item-thumbnails?params=%5B%7BassetId:{v}%7D%5D"
                    af = a.get(ae)
                    if af.status_code == 200:
                        ag = af.json()
                        ah = ag[0].get("thumbnailUrl")
                        x["fields"].append({"name": "URL", "value": f"https://roblox.com/library/{v}"})
                        x["fields"].append({"name": "Thumbnail URL", "value": f"{ah}"})
                    n(h, x)
        else:
            print(f"Could not retrieve asset details for asset ID {v}")
    except Exception as ai:
        print(f"Error occurred: {ai}")
    j += 1
    if j % 10000 == 0:
        aj = c.datetime.now() - k
        ak = {"title": "Asset Check Count", "color": 0xFF4500,
              "description": f"{j} assets checked so far. Latest asset ID: {v}\nTime to scan 10000 assets: {aj}"}
        n(i, ak)


# Calculate the number of processes to use for approximately 95% CPU usage
cpu_count = multiprocessing.cpu_count()
target_cpu_usage = 0.95
num_processes = int(target_cpu_usage * cpu_count)

# Sequentially iterate through asset IDs
for v in range(d, e + 1):
    if v not in g:
        u(v)
        g.add(v)

# Split the range of asset IDs into chunks to utilize multiple cores
chunk_size = (e - d + 1) // num_processes
chunks = [(d + i * chunk_size, d + (i + 1) * chunk_size - 1) for i in range(num_processes)]

# Use a multiprocessing Pool to concurrently process the chunks
if __name__ == '__main__':
    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(u, chunks)
