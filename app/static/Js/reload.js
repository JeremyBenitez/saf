// Intervalo de recarga automática en milisegundos (21 minutos)
const RELOAD_INTERVAL = 21 * 60 * 1000; // 21 minutos

// Función para actualizar la información de la recarga
function updateReloadInfo() {
    const lastAutoReload = localStorage.getItem('lastAutoReload');
    const nextReload = RELOAD_INTERVAL - (Date.now() - lastAutoReload);

    // Convertir el tiempo restante a minutos y segundos
    const minutosRestantes = Math.floor(nextReload / 1000 / 60);
    const segundosRestantes = Math.floor((nextReload / 1000) % 60);
    
    // Mostrar la última recarga automática y el tiempo restante
    document.getElementById('lastReload').textContent = `Última recarga automática: ${lastAutoReload ? new Date(parseInt(lastAutoReload)).toLocaleTimeString() : 'Aún no ha habido recarga automática'}`;
    document.getElementById('nextReload').textContent = `Próxima recarga automática: ${minutosRestantes} minutos y ${segundosRestantes} segundos`;
}

// Función de recarga automática
function autoReload() {
    // Guardar el tiempo actual de la última recarga automática
    localStorage.setItem('lastAutoReload', Date.now());
    
    // Recargar la página
    location.reload();
}

// Configurar la recarga automática solo si han pasado más de RELOAD_INTERVAL desde la última recarga
const lastAutoReload = localStorage.getItem('lastAutoReload');
if (!lastAutoReload || Date.now() - lastAutoReload > RELOAD_INTERVAL) {
    // Si no hay una recarga registrada o ha pasado el intervalo, recargar ahora
    autoReload();
} else {
    // Si hay una recarga reciente, mostrar la información y programar la próxima recarga
    updateReloadInfo();
    setTimeout(autoReload, RELOAD_INTERVAL - (Date.now() - lastAutoReload));
}

// Actualizar la información de recarga cada segundo
setInterval(updateReloadInfo, 1000);
