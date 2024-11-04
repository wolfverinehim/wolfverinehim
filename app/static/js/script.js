document.addEventListener("DOMContentLoaded", () => {
    const connectWalletButton = document.getElementById("connect-wallet");
    const progressText = document.getElementById("progress-text");

    // Conectar la wallet
    connectWalletButton.addEventListener("click", async () => {
        try {
            const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
            const walletAddress = accounts[0];
            alert("Wallet conectada: " + walletAddress);
            // Aquí podrías realizar más acciones, como enviar el walletAddress al backend si fuera necesario
        } catch (error) {
            console.error("Error al conectar la wallet:", error);
        }
    });

    // Obtener el progreso de donaciones desde la API
    async function fetchDonationProgress() {
        try {
            const response = await fetch("/donation/progress");
            if (!response.ok) throw new Error("Error al obtener el progreso de donaciones");
            
            const data = await response.json();
            const progress = data.donation; // Supongamos que la API devuelve un campo 'donation'
            const goal = data.goal; // Supongamos que la API devuelve un campo 'goal'
            progressText.textContent = `${progress} / ${goal}`;
        } catch (error) {
            console.error("Error al obtener el progreso de donaciones:", error);
        }
    }

    // Llamar a fetchDonationProgress cuando se carga la página
    fetchDonationProgress();
});
