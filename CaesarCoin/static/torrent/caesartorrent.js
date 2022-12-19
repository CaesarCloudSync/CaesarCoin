const client = new WebTorrent()
function downloadBlob(blob, name = 'file.txt') {
  // Convert your blob into a Blob URL (a special url that points to an object in the browser's memory)
  const blobUrl = URL.createObjectURL(blob);

  // Create a link element
  const link = document.createElement("a");

  // Set link's href to point to the Blob URL
  link.href = blobUrl;
  link.download = name;

  // Append link to the body
  document.body.appendChild(link);

  // Dispatch click event on the link
  // This is necessary as link.click() does not work on the latest firefox
  link.dispatchEvent(
    new MouseEvent('click', { 
      bubbles: true, 
      cancelable: true, 
      view: window 
    })
  );

  // Remove link from body
  document.body.removeChild(link);
}

// Usage
//let jsonBlob = new Blob(['{"name": "test"}'])

client.on('error', function (err) {
  console.error('ERROR: ' + err.message)
})

document.querySelector('form').addEventListener('submit', async function (e) {
  e.preventDefault() // Prevent page refresh

  const filename = document.querySelector('form input[name=torrentId]').value
  companyname = "Google"
  contributorname = "palondomus"
  quotaname = "Googleman Text Classification"
  //filename = "main.jpeg"
  console.log("Hi")
  const signingresp = await axios.post('http://127.0.0.1:5000/contributorsignin',json={"contributor":contributorname,"email":"amari.lawal05@gmail.com","password":"kya63amari"})
  //const torrentId = "https://webtorrent.io/torrents/sintel.torrent"
  const config = {
      headers: { Authorization: `Bearer ${signingresp.data.access_token}` }
  };
  const torrentmagneturi = await axios.post('http://127.0.0.1:5000/getmagneturi',json={"companyname":companyname,"quotaname":quotaname,"torrentfilename":filename},config)

  const torrentId = torrentmagneturi.data.torrentmagneturi
  log('Adding ' + torrentId)
  client.add(torrentId, onTorrent)
})

function onTorrent (torrent) {
  
  log('Got torrent metadata!')
  log(
    'Torrent info hash: ' + torrent.infoHash + ' ' +
    '<a href="' + torrent.magnetURI + '" target="_blank">[Magnet URI]</a> ' +
    '<a href="' + torrent.torrentFileBlobURL + '" target="_blank" download="' + torrent.name + '.torrent">[Download .torrent]</a>'
  )

  // Print out progress every 5 seconds
  const interval = setInterval(function () {
    log('Progress: ' + (torrent.progress * 100).toFixed(1) + '%')
  }, 5000)

  torrent.on('done', function () {
    log('Progress: 100%')
    clearInterval(interval)
  })
  //console.log(torrent)
  // Render all files into to the page
  torrent.files.forEach(function (file) {
    const filename = document.querySelector('form input[name=torrentId]').value
    console.log()
    if (!file.name.includes("jpeg") && !file.name.includes("png")){
        file.getBlob(function callback (err, blob) {downloadBlob(blob, filename);})
    }
    else {
    file.appendTo('.log')
    log('(Blob URLs only work if the file is loaded from a server. "http//localhost" works. "file://" does not.)')
    file.getBlobURL(function (err, url) {
      if (err) return log(err.message)
      log('File done.')
      log('<a href="' + url + '">Download full file: ' + file.name + '</a>')
    })}
  })
}

function log (str) {
  const p = document.createElement('p')
  p.innerHTML = str
  document.querySelector('.log').appendChild(p)
}