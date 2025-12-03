export async function uploadFile(file) {
  const form = new FormData();
  form.append("file", file);

  const res = await fetch("/process", {
    method: "POST",
    body: form
  });

  return res.json();
}
