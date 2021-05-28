function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/notes";
  });
}
function stopVol(userId) {
  fetch("/stop-vol", {
    method: "POST",
    body: JSON.stringify({userId: userId}),}).then((_res)=> {
      window.location.href = "/personal-page"
  })


}