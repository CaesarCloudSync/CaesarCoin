// ************************ Drag and drop ***************** //
let dropArea = document.getElementById("drop-area")
const client = new WebTorrent()
// Prevent default drag behaviors
;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
  dropArea.addEventListener(eventName, preventDefaults, false)   
  document.body.addEventListener(eventName, preventDefaults, false)
})

// Highlight drop area when item is dragged over it
;['dragenter', 'dragover'].forEach(eventName => {
  dropArea.addEventListener(eventName, highlight, false)
})

;['dragleave', 'drop'].forEach(eventName => {
  dropArea.addEventListener(eventName, unhighlight, false)
})

// Handle dropped files
dropArea.addEventListener('drop', handleDrop, false)

function preventDefaults (e) {
  e.preventDefault()
  e.stopPropagation()
}

function highlight(e) {
  dropArea.classList.add('highlight')
}

function unhighlight(e) {
  dropArea.classList.remove('active')
}

function handleDrop(e) {
  var dt = e.dataTransfer
  var files = dt.files

  handleFiles(files)
}

let uploadProgress = []
let progressBar = document.getElementById('progress-bar')

function initializeProgress(numFiles) {
  progressBar.value = 0
  uploadProgress = []

  for(let i = numFiles; i > 0; i--) {
    uploadProgress.push(0)
  }
}

function updateProgress(fileNumber, percent) {
  uploadProgress[fileNumber] = percent
  let total = uploadProgress.reduce((tot, curr) => tot + curr, 0) / uploadProgress.length
  progressBar.value = total
}

function handleFiles(files) {
  files = [...files]
  console.log(files)
  initializeProgress(files.length)
  console.log("Before")
  files.forEach(caesartorrent)
  
  files.forEach(previewFile)
}

function previewFile(file) {
  let reader = new FileReader()
  reader.readAsDataURL(file)
  reader.onloadend = function() {
    let img = document.createElement('img')
    img.src = reader.result
    document.getElementById('gallery').appendChild(img)
  }
}

async function caesartorrent(file, i) {
  let files = [file]
  console.log(files)
  companyname = "Google"
  contributorname = "palondomus"
  quotaname = "Googleman Text Classification"
  const signingresp = await axios.post('http://127.0.0.1:5000/contributorsignin',json={"contributor":contributorname,"email":"amari.lawal05@gmail.com","password":"kya63amari"})

  console.log(signingresp.data.access_token)

const config = {
    headers: { Authorization: `Bearer ${signingresp.data.access_token}` }
};

client.seed(files, function(torrent){
  try{
  console.log("Client seeding: " + torrent.magnetURI)
  axios.post('http://127.0.0.1:5000/storemagneturi',json={"companyname":companyname,"quotaname":quotaname,"torrentfilename":files[0]["name"],"torrentmagneturi":torrent.magnetURI},config)
  .then((resp) => console.log(resp.data))}
  catch(err){
    console.log(err)
  }
})



}
// New Function where after caesartorrent has been called 

