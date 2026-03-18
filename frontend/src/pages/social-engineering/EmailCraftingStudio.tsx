import { useState } from 'react';
import { useEmailCraft, useSpearPhishing, useFakeLogin, useTrackingLink } from '../../hooks/useAdvancedTools';
import { Mail, Code, Eye, Link as LinkIcon, Loader2, Copy } from 'lucide-react';
import Badge from '../../components/ui/Badge';

export default function EmailCraftingStudio() {
  const [activeTab, setActiveTab] = useState<'craft' | 'spear' | 'fake-login' | 'tracking'>('craft');
  const [targetInfo, setTargetInfo] = useState({ name: '', company: '', position: '' });
  const [payloadLink, setPayloadLink] = useState('https://malicious.example.com/payload');
  const [templateType, setTemplateType] = useState('urgent_security');
  const [brand, setBrand] = useState('microsoft');
  const [trackingUrl, setTrackingUrl] = useState('');

  const { mutate: craftEmail, data: email, isPending: isCrafting } = useEmailCraft();
  const { mutate: craftSpear, data: spearEmail, isPending: isSpearing } = useSpearPhishing();
  const { mutate: createFakeLogin, data: fakeLogin, isPending: isCreatingFake } = useFakeLogin();
  const { mutate: createTracking, data: tracking, isPending: isCreatingTracking } = useTrackingLink();

  const handleCraft = () => {
    craftEmail({ target_info: targetInfo, payload_link: payloadLink, template_type: templateType });
  };

  const handleSpear = () => {
    craftSpear(targetInfo);
  };

  const handleFakeLogin = () => {
    createFakeLogin(brand);
  };

  const handleTracking = () => {
    createTracking(trackingUrl);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const templates = [
    { value: 'urgent_security', label: 'Urgent Security Alert' },
    { value: 'password_reset', label: 'Password Reset' },
    { value: 'invoice', label: 'Invoice/Payment' },
    { value: 'hr_notice', label: 'HR Notice' },
    { value: 'it_support', label: 'IT Support' }
  ];

  const brands = ['microsoft', 'google', 'facebook', 'linkedin', 'dropbox', 'github'];

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500/20 to-pink-500/20 
                         border border-purple-500/30 flex items-center justify-center">
            <Mail className="w-5 h-5 text-purple-400" />
          </div>
          Email Crafting Studio
        </h1>
        <p className="text-gray-400 mt-1 ml-13">Professional phishing email templates and fake login pages</p>
      </div>

      <div className="flex gap-2 overflow-x-auto pb-2">
        {[
          { id: 'craft', label: 'Email Craft', icon: Mail },
          { id: 'spear', label: 'Spear Phishing', icon: Mail },
          { id: 'fake-login', label: 'Fake Login', icon: Code },
          { id: 'tracking', label: 'Tracking Link', icon: LinkIcon }
        ].map(tab => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-lg whitespace-nowrap transition-all duration-300 ${
                activeTab === tab.id
                  ? 'bg-gradient-to-r from-purple-500/20 to-pink-500/20 text-purple-400 border border-purple-500/50 shadow-lg shadow-purple-500/20'
                  : 'bg-gray-800/50 text-gray-400 hover:text-white hover:bg-gray-800 border border-gray-700/50'
              }`}
            >
              <Icon className="w-4 h-4" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {activeTab === 'craft' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="glass-panel p-6 rounded-xl border border-gray-800 hover:border-purple-500/30 transition-all duration-300 space-y-4">
            <h3 className="text-lg font-semibold text-white flex items-center gap-2">
              <span className="text-purple-500">⚙️</span> Email Configuration
            </h3>
            <input
              type="text"
              value={targetInfo.name}
              onChange={(e) => setTargetInfo({ ...targetInfo, name: e.target.value })}
              placeholder="Target Name"
              className="input-field"
            />
            <input
              type="text"
              value={targetInfo.company}
              onChange={(e) => setTargetInfo({ ...targetInfo, company: e.target.value })}
              placeholder="Company"
              className="input-field"
            />
            <input
              type="text"
              value={payloadLink}
              onChange={(e) => setPayloadLink(e.target.value)}
              placeholder="Payload Link"
              className="input-field"
            />
            <select value={templateType} onChange={(e) => setTemplateType(e.target.value)} className="input-field">
              {templates.map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
            </select>
            <button onClick={handleCraft} disabled={isCrafting} className="w-full px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 
                     text-white font-semibold rounded-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed
                     flex items-center justify-center gap-2 shadow-lg hover:shadow-purple-500/50">
              {isCrafting ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Generate Email'}
            </button>
          </div>

          {email && (
            <div className="glass-panel p-6 rounded-xl border border-gray-800 relative overflow-hidden space-y-4">
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-purple-500/50 to-transparent opacity-50"></div>
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold text-white">Generated Email</h3>
                <button onClick={() => copyToClipboard(email.body)} className="px-3 py-1.5 bg-gray-800 hover:bg-gray-700 text-cyan-400 rounded-lg transition-all duration-300 border border-gray-700 hover:border-cyan-500/50 flex items-center gap-2 text-sm">
                  <Copy className="w-4 h-4" />
                  Copy
                </button>
              </div>
              <div className="space-y-2">
                <div>
                  <div className="text-sm text-gray-400">Subject</div>
                  <div className="text-white font-medium">{email.subject}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-400">Body</div>
                  <div className="p-3 bg-gray-800/50 rounded text-sm text-gray-300 whitespace-pre-wrap max-h-96 overflow-y-auto">
                    {email.body}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {activeTab === 'spear' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="glass-panel p-6 rounded-xl border border-gray-800 hover:border-pink-500/30 transition-all duration-300 space-y-4">
            <h3 className="text-lg font-semibold text-white flex items-center gap-2">
              <span className="text-pink-500">🎯</span> Target Information
            </h3>
            <input
              type="text"
              value={targetInfo.name}
              onChange={(e) => setTargetInfo({ ...targetInfo, name: e.target.value })}
              placeholder="Full Name"
              className="input-field"
            />
            <input
              type="text"
              value={targetInfo.company}
              onChange={(e) => setTargetInfo({ ...targetInfo, company: e.target.value })}
              placeholder="Company"
              className="input-field"
            />
            <input
              type="text"
              value={targetInfo.position}
              onChange={(e) => setTargetInfo({ ...targetInfo, position: e.target.value })}
              placeholder="Position"
              className="input-field"
            />
            <button onClick={handleSpear} disabled={isSpearing} className="w-full px-6 py-3 bg-gradient-to-r from-pink-500 to-red-500 hover:from-pink-600 hover:to-red-600 
                     text-white font-semibold rounded-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed
                     flex items-center justify-center gap-2 shadow-lg hover:shadow-pink-500/50">
              {isSpearing ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Craft Spear-Phishing Email'}
            </button>
          </div>

          {spearEmail && (
            <div className="glass-panel p-6 rounded-xl border border-gray-800 relative overflow-hidden space-y-4">
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-pink-500/50 to-transparent opacity-50"></div>
              <h3 className="text-lg font-semibold text-white">Spear-Phishing Email</h3>
              <div className="space-y-2">
                <div>
                  <div className="text-sm text-gray-400">Subject</div>
                  <div className="text-white font-medium">{spearEmail.subject}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-400">Body</div>
                  <div className="p-3 bg-gray-800/50 rounded text-sm text-gray-300 whitespace-pre-wrap max-h-96 overflow-y-auto">
                    {spearEmail.body}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {activeTab === 'fake-login' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="glass-panel p-6 rounded-xl border border-gray-800 hover:border-cyan-500/30 transition-all duration-300 space-y-4">
            <h3 className="text-lg font-semibold text-white flex items-center gap-2">
              <span className="text-cyan-500">🔐</span> Fake Login Page
            </h3>
            <select value={brand} onChange={(e) => setBrand(e.target.value)} className="input-field">
              {brands.map(b => <option key={b} value={b}>{b.charAt(0).toUpperCase() + b.slice(1)}</option>)}
            </select>
            <button onClick={handleFakeLogin} disabled={isCreatingFake} className="w-full px-6 py-3 bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600 
                     text-white font-semibold rounded-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed
                     flex items-center justify-center gap-2 shadow-lg hover:shadow-cyan-500/50">
              {isCreatingFake ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Generate Fake Login'}
            </button>
          </div>

          {fakeLogin && (
            <div className="glass-panel p-6 rounded-xl border border-gray-800 relative overflow-hidden space-y-4">
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-cyan-500/50 to-transparent opacity-50"></div>
              <h3 className="text-lg font-semibold text-white">Generated Page</h3>
              <div className="space-y-2">
                <div>
                  <div className="text-sm text-gray-400">URL</div>
                  <div className="flex items-center gap-2">
                    <code className="flex-1 p-2 bg-gray-800/50 rounded text-sm text-cyan-400">{fakeLogin.url}</code>
                    <button onClick={() => copyToClipboard(fakeLogin.url)} className="px-3 py-2 bg-gray-800 hover:bg-gray-700 text-cyan-400 rounded-lg transition-all duration-300 border border-gray-700 hover:border-cyan-500/50">
                      <Copy className="w-4 h-4" />
                    </button>
                  </div>
                </div>
                <div>
                  <div className="text-sm text-gray-400">HTML Preview</div>
                  <div className="p-3 bg-gray-800/50 rounded text-xs text-gray-300 font-mono max-h-96 overflow-y-auto">
                    {fakeLogin.html}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {activeTab === 'tracking' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="glass-panel p-6 rounded-xl border border-gray-800 hover:border-green-500/30 transition-all duration-300 space-y-4">
            <h3 className="text-lg font-semibold text-white flex items-center gap-2">
              <span className="text-green-500">🔗</span> Tracking Link Generator
            </h3>
            <input
              type="text"
              value={trackingUrl}
              onChange={(e) => setTrackingUrl(e.target.value)}
              placeholder="https://target-url.com"
              className="input-field"
            />
            <button onClick={handleTracking} disabled={isCreatingTracking} className="w-full px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 
                     text-white font-semibold rounded-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed
                     flex items-center justify-center gap-2 shadow-lg hover:shadow-green-500/50">
              {isCreatingTracking ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Generate Tracking Link'}
            </button>
          </div>

          {tracking && (
            <div className="glass-panel p-6 rounded-xl border border-gray-800 relative overflow-hidden space-y-4">
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-green-500/50 to-transparent opacity-50"></div>
              <h3 className="text-lg font-semibold text-white">Tracking Link</h3>
              <div className="space-y-3">
                <div>
                  <div className="text-sm text-gray-400 mb-1">Tracking URL</div>
                  <div className="flex items-center gap-2">
                    <code className="flex-1 p-2 bg-gray-800/50 rounded text-sm text-cyan-400 break-all">
                      {tracking.tracking_url}
                    </code>
                    <button onClick={() => copyToClipboard(tracking.tracking_url)} className="px-3 py-2 bg-gray-800 hover:bg-gray-700 text-green-400 rounded-lg transition-all duration-300 border border-gray-700 hover:border-green-500/50">
                      <Copy className="w-4 h-4" />
                    </button>
                  </div>
                </div>
                <div>
                  <div className="text-sm text-gray-400 mb-1">Tracking ID</div>
                  <Badge variant="info">{tracking.tracking_id}</Badge>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
