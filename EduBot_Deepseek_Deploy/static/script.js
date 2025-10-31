const chatBox = document.getElementById('chat-box');
const form = document.getElementById('chat-form');
const input = document.getElementById('user-input');

function append(role, text){
  const d = document.createElement('div');
  d.className = 'msg ' + role;
  d.textContent = text;
  chatBox.appendChild(d);
  chatBox.scrollTop = chatBox.scrollHeight;
  return d;
}

form.addEventListener('submit', async (e)=>{
  e.preventDefault();
  const txt = input.value.trim();
  if(!txt) return;
  append('user', txt);
  input.value = '';
  const placeholder = append('bot','...');

  try{
    const res = await fetch('/chat', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({message: txt})
    });
    const data = await res.json();
    if(data.reply){
      placeholder.textContent = data.reply;
    } else if (data.error){
      placeholder.textContent = 'Error: ' + (data.error || 'unknown');
    } else {
      placeholder.textContent = 'Unexpected response';
    }
  } catch(err){
    placeholder.textContent = 'Network error';
    console.error(err);
  }
});
