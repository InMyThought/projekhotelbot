// === HOTELBOT.JS ===
// Versi Full AI (Sudah di-fix POST & Timeout)

import makeWASocket, { 
    DisconnectReason, 
    useMultiFileAuthState 
} from '@whiskeysockets/baileys';
import QRCode from 'qrcode-terminal';
import axios from 'axios';
import fs from 'fs/promises';
import 'dotenv/config';

// === KONFIGURASI BOT ===
const DJANGO_CHAT_API_URL = process.env.DJANGO_CHAT_API_URL || 'http://127.0.0.1:8000/api/chat/';
const ALLOWED_ONLY = process.env.ALLOWED_ONLY === 'true';
const allowedNumbers = process.env.ALLOWED_NUMBERS?.split(',') || [];
const PROMO_ENABLED = process.env.PROMO_ENABLED === 'true';
const PROMO_MESSAGE = process.env.PROMO_MESSAGE || '🎁 Nikmati promo spesial dari Hotel Jaya!';
const PROMO_INTERVAL = parseInt(process.env.PROMO_INTERVAL || '10');
const HISTORY_FILE = 'hotel_history.json';
const MAX_HISTORY = 6;
const WELCOME_IMAGE_URL = process.env.WELCOME_IMAGE_URL || '';

// ================================================
// === FUNGSI PENDUKUNG (DIUBAH KE POST) ===
// ================================================
async function getAIResponseFromDjango(history, message) {
    // Siapkan payload untuk dikirim di body
    const payload = {
        message: message,
        history: JSON.stringify(history)
    };
    
    try {
        // DIUBAH: dari axios.get ke axios.post
        // Argumen kedua adalah payload (body)
        const response = await axios.post(DJANGO_CHAT_API_URL, payload, {
            // DIUBAH: Timeout dinaikkan ke 30 detik sisi client
            timeout: 30000 
        });
        return response.data?.reply || null;
    } catch (err) {
        console.error("❌ [API ERROR]", err.message);
        // Tambahkan logging jika timeout
        if (err.code === 'ECONNABORTED') {
            console.error("❌ Error: Koneksi timeout. Server Django/Gemini terlalu lama merespons.");
        }
        return null; // Mengembalikan null jika API error
    }
}

async function loadHistory() {
    try {
        const data = await fs.readFile(HISTORY_FILE, 'utf-8');
        return JSON.parse(data);
    } catch {
        console.log(`File ${HISTORY_FILE} tidak ditemukan, membuat baru...`);
        return {};
    }
}

async function saveHistory(history) {
    try {
        await fs.writeFile(HISTORY_FILE, JSON.stringify(history, null, 2));
    } catch (error) {
        console.error("⚠️ Gagal menyimpan history:", error.message);
    }
}

// === INTI BOT ===
async function startBot() {
    console.log("🧠 Menyiapkan sistem Hotel Jaya...");
    await new Promise(r => setTimeout(r, 2000)); 

    const { state, saveCreds } = await useMultiFileAuthState('./auth_info_baileys');
    let chatHistory = await loadHistory();

    const sock = makeWASocket({
        auth: state,
        browser: ['Hotel Jaya Bot', 'Chrome', '1.0.0'],
        printQRInTerminal: false
    });

    // ... (Logika connection.update dan creds.update tetap sama) ...
    sock.ev.on('connection.update', async ({ connection, lastDisconnect, qr }) => {
        if (qr) {
            console.log('\n📱 Scan QR ini untuk login WhatsApp:');
            QRCode.generate(qr, { small: true });
        }
        if (connection === 'open') {
            console.log('✅ Bot Hotel Jaya aktif dan siap melayani tamu!');
            await sock.sendPresenceUpdate('available');
        }
        if (connection === 'close') {
            const reason = lastDisconnect?.error?.output?.statusCode;
            if (reason !== DisconnectReason.loggedOut) {
                console.log('🔄 Koneksi terputus, mencoba menghubungkan ulang...');
                setTimeout(startBot, 3000);
            } else {
                console.log('🛑 Koneksi terputus permanen (Logged Out). Hapus folder auth_info_baileys dan scan ulang.');
            }
        }
    });
    sock.ev.on('creds.update', saveCreds);

    // ================================================
    // === PESAN MASUK (Logika FULL AI) ===
    // ================================================
    sock.ev.on('messages.upsert', async ({ messages }) => {
        const msg = messages[0];
        if (!msg.message || msg.key.fromMe) return;

        const sender = msg.key.remoteJid;
        const text = msg.message.conversation || msg.message.extendedTextMessage?.text;
        if (!text) return;

        const senderNumber = sender.split('@')[0];
        const isAllowed = allowedNumbers.includes(senderNumber);

        if (ALLOWED_ONLY && !isAllowed) {
            console.log(`🚫 Pesan diabaikan dari nomor tidak diizinkan: ${senderNumber}`);
            return;
        }

        console.log(`\n📩 [${senderNumber}] ➤ ${text}`);

        try {
            await sock.sendPresenceUpdate('composing', sender);

            if (!chatHistory[senderNumber]) chatHistory[senderNumber] = [];
            const history = chatHistory[senderNumber].slice(-MAX_HISTORY * 2);

            // === Logika Sapaan (Pesan Pertama) ===
            if (history.length === 0) {
                const welcomeCaption = "👋 Halo! Saya Jaya, asisten virtual Hotel Maju Jaya.\n\n" +
                                       "Ada yang bisa saya bantu terkait info kamar, fasilitas, atau reservasi? 😊";
                
                let replyMessage;
                if (WELCOME_IMAGE_URL) {
                    console.log("🖼️ Mengirim sapaan selamat datang dengan gambar...");
                    replyMessage = { 
                        image: { url: WELCOME_IMAGE_URL },
                        caption: welcomeCaption 
                    };
                } else {
                    console.log("💬 Mengirim sapaan selamat datang (teks)...");
                    replyMessage = { text: welcomeCaption };
                }

                await new Promise(r => setTimeout(r, 1000));
                await sock.sendMessage(sender, replyMessage);

                // Simpan sapaan ke riwayat
                history.push({ role: 'user', text });
                history.push({ role: 'model', text: welcomeCaption }); 
                chatHistory[senderNumber] = history;
                await saveHistory(chatHistory);
                
                return; // Hentikan, tunggu balasan user
            }

            // === Logika AI (Untuk semua pesan setelah sapaan) ===
            await new Promise(r => setTimeout(r, Math.random() * 2000 + 800));

            const reply = await getAIResponseFromDjango(history, text);
            const finalReply = reply || "🙏 Maaf, sistem sedang sibuk. Silakan coba lagi beberapa saat lagi.";

            await sock.sendMessage(sender, { text: finalReply });
            console.log(`🤖 [Balasan AI] ${finalReply}`);

            // Simpan ke riwayat
            history.push({ role: 'user', text });
            history.push({ role: 'model', text: finalReply });
            chatHistory[senderNumber] = history;
            await saveHistory(chatHistory);

            // ... (Logika Promo tetap sama) ...
            if (PROMO_ENABLED && (history.length / 2) % PROMO_INTERVAL === 0) {
                await new Promise(r => setTimeout(r, 1000));
                await sock.sendMessage(sender, { text: PROMO_MESSAGE });
                console.log("🎁 Promo terkirim otomatis.");
            }

        } catch (err) {
            console.error('⚠️ Error internal saat proses pesan:', err.message);
        } finally {
            await sock.sendPresenceUpdate('available', sender);
        }
    });
}

// Memulai bot
startBot();