document.addEventListener("DOMContentLoaded", () => {

    const lista = document.getElementById("lista");
    const listaTickets = document.getElementById("listaTickets");

    const formAtivo = document.getElementById("formAtivo");
    const formTicket = document.getElementById("formTicket");

    const suporteBox = document.getElementById("suporteBox");
    const btnSuporte = document.getElementById("btnSuporte");

    const selectAtivo = document.getElementById("id_ativo");

    let editandoId = null;

    // -------- ATIVOS --------
    async function carregarAtivos() {
        const res = await fetch("/ativos");
        const ativos = await res.json();

        lista.innerHTML = "";
        selectAtivo.innerHTML = "";

        ativos.forEach(a => {

            const li = document.createElement("li");
            li.innerHTML = `
                <strong>ID:</strong> ${a.id_ativo} |
                <strong>Nome:</strong> ${a.nome_ativo} |
                <strong>Categoria:</strong> ${a.tipo_categoria || "-"} |
                <strong>Aquisição:</strong> ${a.data_aquisicao || "-"} |
                <strong>Status:</strong> ${a.status_governanca || "-"} |
                <strong>Última falha:</strong> ${a.ultima_falha || "Nunca"}
                <button onclick="editar(${a.id_ativo})">Editar</button>
                <button onclick="excluir(${a.id_ativo})">Excluir</button>
            `;
            lista.appendChild(li);

            const option = document.createElement("option");
            option.value = a.id_ativo;
            option.textContent = `${a.id_ativo} - ${a.nome_ativo}`;
            selectAtivo.appendChild(option);
        });
    }

    // -------- SALVAR ATIVO --------
    formAtivo.addEventListener("submit", async (e) => {
        e.preventDefault();

        const data = {
            nome_ativo: document.getElementById("nome_ativo").value,
            tipo_categoria: document.getElementById("tipo_categoria").value,
            data_aquisicao: document.getElementById("data_aquisicao").value,
            status_governanca: document.getElementById("status_governanca").value
        };

        if (editandoId !== null) {
            await fetch(`/ativos/${editandoId}`, {
                method: "PUT",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            });

            editandoId = null; // 🔥 MUITO IMPORTANTE
        } else {
            await fetch("/ativos", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            });
        }

        formAtivo.reset();
        await carregarAtivos();
    });

    // -------- EDITAR --------
    window.editar = async (id) => {
        const res = await fetch("/ativos");
        const ativos = await res.json();
        const a = ativos.find(x => x.id_ativo === id);

        document.getElementById("nome_ativo").value = a.nome_ativo;
        document.getElementById("tipo_categoria").value = a.tipo_categoria;
        document.getElementById("data_aquisicao").value = a.data_aquisicao;
        document.getElementById("status_governanca").value = a.status_governanca;

        editandoId = id;
    };

    // -------- EXCLUIR --------
    window.excluir = async (id) => {
        if (confirm("Deseja excluir este ativo?")) {
            await fetch(`/ativos/${id}`, { method: "DELETE" });
            await carregarAtivos();
        }
    };

    // -------- SUPORTE --------
    btnSuporte.addEventListener("click", () => {
        suporteBox.style.display =
            suporteBox.style.display === "none" ? "block" : "none";
    });

    formTicket.addEventListener("submit", async (e) => {
        e.preventDefault();

        const data = {
            id_ativo: selectAtivo.value,
            nivel_criticidade: document.getElementById("nivel_criticidade").value,
            descricao_erro: document.getElementById("descricao_erro").value
        };

        await fetch("/tickets", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        });

        formTicket.reset();
        await carregarTickets();
	await carregarAtivos();
    });

    // -------- TICKETS --------
    async function carregarTickets() {
        const res = await fetch("/tickets");
        const tickets = await res.json();

        listaTickets.innerHTML = "";

        tickets.forEach(t => {

            let botao = "";

            if (t.status_suporte === "Ticket aberto") {
                botao = `<button onclick="mudarStatus(${t.id_ticket}, 'Em manutenção')">Iniciar manutenção</button>`;
            } else if (t.status_suporte === "Em manutenção") {
                botao = `<button onclick="mudarStatus(${t.id_ticket}, 'Finalizado')">Finalizar</button>`;
            }

            const li = document.createElement("li");
            li.innerHTML = `
                🎫 <strong>${t.nome_ativo}</strong> | ${t.nivel_criticidade}
                <button onclick="toggleDescricao(${t.id_ticket})">Descrição</button>
                ${botao}
                <div id="desc-${t.id_ticket}" style="display:none;">
                    ${t.descricao_erro}
                </div>
            `;
            listaTickets.appendChild(li);
        });
    }

    // -------- MOSTRAR DESCRIÇÃO --------
    window.toggleDescricao = (id) => {
        const el = document.getElementById(`desc-${id}`);
        el.style.display = el.style.display === "none" ? "block" : "none";
    };

    // -------- STATUS --------
    window.mudarStatus = async (id, status) => {
        await fetch(`/tickets/${id}`, {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ status_suporte: status })
        });

        await carregarTickets();
    };

    // -------- INIT --------
    carregarAtivos();
    carregarTickets();
});