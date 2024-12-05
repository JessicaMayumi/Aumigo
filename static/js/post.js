function saveContent(event) {
    console.log("Função saveContent chamada");
    event.preventDefault();  

    const content = document.getElementById('post-content').innerHTML; 
    const titulo = document.getElementById('input-username').value;  
    const status = document.querySelector('input[name="status"]:checked')?.value;  
    const visibilidade = document.querySelector('input[name="visibilidade"]:checked')?.value;  

    console.log({ titulo, status, visibilidade, conteudo: content });

    const postData = {
        titulo: titulo,
        status: status,
        visibilidade: visibilidade,
        conteudo: content
    };

    fetch('/addPost', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'  
        },
        body: JSON.stringify(postData)  
    })
    .then(response => {
        // Verifica se a resposta é válida (status 200-299)
        if (!response.ok) {
            throw new Error('Erro no servidor ao salvar o post');
        }
        return response.json();  
    })
    .then(data => {
        console.log(data);  

        if (data.erro) {
            alert('Erro: ' + data.erro);  
        } else {
            alert('Post salvo com sucesso!'); 

            window.location.href = "/perfil";  
        }
    })
    .catch(error => {
        console.error('Erro ao salvar post:', error);  
        alert('Houve um problema ao salvar o post. Tente novamente.');
    });
}




