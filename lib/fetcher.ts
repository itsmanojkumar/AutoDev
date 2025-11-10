import axios from 'axios';


export async function postGenerate(prompt: string) {
const base = process.env.NEXT_PUBLIC_AI_API_URL || '/api/ai';
const res = await axios.post(`${base}/generate`, { prompt });
return res.data;
}