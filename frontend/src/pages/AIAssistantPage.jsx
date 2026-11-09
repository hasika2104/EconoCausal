import React, { useState, useRef, useEffect } from 'react';
import {
  Bot,
  User,
  Send,
  Sparkles,
  RefreshCw,
  TrendingUp,
  AlertCircle,
  HelpCircle,
  SlidersHorizontal,
  DollarSign,
  ChevronRight,
  Database
} from 'lucide-react';
import { sendChatMessage } from '../services/api';

const DEFAULT_QUESTIONS = [
  "Which product has the highest demand?",
  "What happens if I increase the price by 5%?",
  "Which products may need price adjustments?",
  "What is the estimated effect of price on demand?",
  "Which products generate the most revenue?",
  "Which products have the highest profit?",
  "Explain my sales trends.",
  "Compare two pricing scenarios.",
  "Summarize my dataset."
];

export default function AIAssistantPage({ onNavigate, lang = 'en' }) {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: lang === 'te' 
        ? 'నమస్కారం! నేను మీ **EconoCausal AI ప్రైసింగ్ అనలిస్ట్‌ను**. మీ స్టోర్ సేల్స్ డేటా, డబుల్ మెషిన్ లెర్నింగ్ ఎలాస్టిసిటీ ఫలితాలు లేదా ధరల మార్పులపై ఏదైనా ప్రశ్న అడగండి.'
        : 'Welcome! I am your **EconoCausal Retail Pricing Analyst**. I am grounded in your retail sales observations, Double ML causal elasticity estimates, and shelf inventory constraints. How can I assist your pricing strategy today?',
      source: 'EconoCausal Engine'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (queryText = null) => {
    const textToSend = queryText || input;
    if (!textToSend.trim() || loading) return;

    const userMsg = { role: 'user', content: textToSend };
    setMessages((prev) => [...prev, userMsg]);
    if (!queryText) setInput('');
    setLoading(true);

    try {
      // Build history
      const history = messages.slice(-6).map((m) => ({ role: m.role, content: m.content }));
      const res = await sendChatMessage(textToSend, history);

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: res.reply,
          data_points: res.data_points,
          source: res.source || 'EconoCausal Analytical Engine'
        }
      ]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'Sorry, I encountered an issue connecting to the pricing engine. Please verify the backend service is running on port 8000.',
          source: 'System Error'
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="bg-white border border-slate-200/90 rounded-2xl p-6 shadow-xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <div className="w-9 h-9 rounded-xl bg-emerald-100 text-emerald-800 flex items-center justify-center">
              <Bot className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-slate-900">
                {lang === 'te' ? 'AI రిటైల్ ప్రైసింగ్ అసిస్టెంట్' : 'AI Retail Pricing Assistant'}
              </h1>
              <p className="text-xs text-slate-500 font-medium">
                {lang === 'te' 
                  ? '73,100 రిటైల్ రికార్డులు మరియు DML కాజల్ ఫలితాలతో అనుసంధానించబడింది'
                  : 'Grounded in 73,100 store-day observations and Double ML causal parameters'}
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold">
            <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
            <span>Retail Analyst Persona</span>
          </span>
        </div>
      </div>

      {/* Suggested Questions Grid */}
      <div className="bg-slate-50 border border-slate-200/80 rounded-2xl p-4">
        <div className="text-xs font-bold text-slate-600 uppercase tracking-wider mb-2 flex items-center gap-1.5">
          <HelpCircle className="w-3.5 h-3.5 text-emerald-600" />
          <span>{lang === 'te' ? 'సిఫార్సు చేయబడిన ప్రశ్నలు (Quick Prompts):' : 'Suggested Analytical Inquiries:'}</span>
        </div>
        <div className="flex flex-wrap gap-2">
          {DEFAULT_QUESTIONS.map((q, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(q)}
              disabled={loading}
              className="text-left px-3 py-1.5 bg-white hover:bg-emerald-50 hover:text-emerald-800 hover:border-emerald-200 border border-slate-200/90 rounded-lg text-xs font-medium text-slate-700 transition-all shadow-2xs"
            >
              {q}
            </button>
          ))}
        </div>
      </div>

      {/* Chat Messages Display */}
      <div className="bg-white border border-slate-200/90 rounded-2xl p-6 shadow-xs flex flex-col min-h-[480px] max-h-[620px]">
        <div className="flex-1 overflow-y-auto space-y-4 pr-2">
          {messages.map((msg, idx) => {
            const isUser = msg.role === 'user';
            return (
              <div key={idx} className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}>
                {!isUser && (
                  <div className="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-800 flex items-center justify-center shrink-0 mt-1">
                    <Bot className="w-4 h-4" />
                  </div>
                )}

                <div
                  className={`max-w-[85%] rounded-2xl p-4 text-xs md:text-sm leading-relaxed ${
                    isUser
                      ? 'bg-emerald-700 text-white rounded-br-none shadow-xs'
                      : 'bg-slate-50 border border-slate-200/80 text-slate-800 rounded-bl-none'
                  }`}
                >
                  <div className="whitespace-pre-line prose prose-sm max-w-none">
                    {msg.content}
                  </div>

                  {!isUser && msg.source && (
                    <div className="mt-2 pt-2 border-t border-slate-200/60 flex items-center justify-between text-[10px] text-slate-400">
                      <span>Source: {msg.source}</span>
                      <span className="font-semibold text-emerald-700">Verified Grounding</span>
                    </div>
                  )}
                </div>

                {isUser && (
                  <div className="w-8 h-8 rounded-lg bg-slate-200 text-slate-700 flex items-center justify-center shrink-0 mt-1">
                    <User className="w-4 h-4" />
                  </div>
                )}
              </div>
            );
          })}

          {loading && (
            <div className="flex gap-3 items-center text-slate-500 text-xs">
              <div className="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-800 flex items-center justify-center shrink-0">
                <RefreshCw className="w-4 h-4 animate-spin text-emerald-600" />
              </div>
              <div className="bg-slate-50 p-3 rounded-xl border border-slate-200/80">
                <span>Evaluating empirical elasticity and retail dataset metrics...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Bar */}
        <div className="mt-4 pt-4 border-t border-slate-100 flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder={
              lang === 'te'
                ? 'ఏదైనా ప్రశ్నను ఇక్కడ అడగండి (ఉదా: 5% ధర పెంచితే ఏమి జరుగుతుంది?)...'
                : 'Ask any pricing question (e.g., Which product generates the most revenue?)...'
            }
            className="flex-1 px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-xs md:text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500"
          />

          <button
            onClick={() => handleSend()}
            disabled={loading || !input.trim()}
            className="px-5 py-3 bg-emerald-700 hover:bg-emerald-800 disabled:bg-slate-300 text-white rounded-xl text-xs md:text-sm font-semibold transition-all flex items-center gap-1.5 shadow-sm"
          >
            <span>Send</span>
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
