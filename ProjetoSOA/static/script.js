const apiProdutos = "http://127.0.0.1:5001/produtos";
const apiCarrinho = "http://127.0.0.1:5002/carrinho";
const apiPagamento = "http://127.0.0.1:5003/pagamento";

// Função para OBTER dados do carrinho (nova função)
async function obterCarrinho() {
    const res = await fetch(apiCarrinho);
    return await res.json();
}
// Limpar carrinho após compra
async function limparCarrinho() {
    try {
        await fetch(apiCarrinho, {
            method: "DELETE"
        });
        console.log("Carrinho limpo com sucesso");
    } catch (error) {
        console.error("Erro ao limpar carrinho:", error);
    }
}
// Função para ATUALIZAR a interface do carrinho (mantém o mesmo nome)
async function atualizarCarrinho() {
    const itens = await obterCarrinho(); // Usa a nova função
    
    const lista = document.getElementById("carrinho");
    lista.innerHTML = "";

    itens.forEach(i => {
        const item = document.createElement("li");
        item.className = "list-group-item d-flex justify-content-between align-items-center";
        item.innerHTML = `${i.nome} - R$ ${i.preco.toFixed(2)}`;
        lista.appendChild(item);
    });
}

async function finalizarPagamento() {
    try {
        const itensCarrinho = await obterCarrinho();
        const total = itensCarrinho.reduce((soma, item) => soma + (item.preco * (item.quantidade || 1)), 0);
        
        const dadosPagamento = { total: total };

        const res = await fetch(apiPagamento, {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dadosPagamento)
        });
        
        const dados = await res.json();

        const msg = document.getElementById("mensagemPagamento");
        msg.innerHTML = `
            <div class="alert alert-${dados.status === 'sucesso' ? 'success' : 'danger'}" role="alert">
            ${dados.mensagem}
            </div>
        `;

        // LIMPAR CARRINHO APÓS PAGAMENTO BEM-SUCEDIDO
        if (dados.status === 'sucesso') {
            await limparCarrinho();
        }

        atualizarCarrinho();
        
    } catch (error) {
        const msg = document.getElementById("mensagemPagamento");
        msg.innerHTML = `
            <div class="alert alert-danger" role="alert">
            Erro: ${error.message}
            </div>
        `;
    }
}

// Restante do código mantém igual...
async function carregarProdutos() {
    const res = await fetch(apiProdutos);
    const produtos = await res.json();

    const lista = document.getElementById("listaProdutos");
    lista.innerHTML = "";

    produtos.forEach(p => {
        const card = document.createElement("div");
        card.className = "col-md-4";

        card.innerHTML = `
            <div class="card shadow-sm h-100">
            <div class="card-body d-flex flex-column">
                <h5 class="card-title">${p.nome}</h5>
                <p class="card-text text-muted">Preço: R$ ${p.preco.toFixed(2)}</p>
                <button class="btn btn-primary mt-auto" onclick="adicionarCarrinho(${p.id})">Adicionar ao Carrinho</button>
            </div>
            </div>
        `;
        lista.appendChild(card);
    });
}

async function adicionarCarrinho(idProduto) {
    await fetch(apiCarrinho, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({id: idProduto})
    });
    atualizarCarrinho();
}

// Inicialização
carregarProdutos();
atualizarCarrinho();