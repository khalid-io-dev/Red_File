import React, { useState } from 'react';
import { Mail, Search, Target, Send, AlertTriangle } from 'lucide-react';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export default function SocialEngineering() {
  const [target, setTarget] = useState('');
  const [targetType, setTargetType] = useState('email');
  const [osintResults, setOsintResults] = useState(null);
  const [email, setEmail] = useState(null);
  const [campaign, setCampaign] = useState({
    name: '',
    target_email: '',
    target_name: '',
    target_company: '',
    template_type: 'urgent_security'
  });
  const [loading, setLoading] = useState(false);

  const gatherOSINT = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(`${API_URL}/social/osint`, {
        target,
        target_type: targetType
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setOsintResults(response.data.data);
    } catch (error) {
      console.error('Error gathering OSINT:', error);
    }
    setLoading(false);
  };

  const craftEmail = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(`${API_URL}/social/email-craft`, {
        target_info: {
          name: campaign.target_name,
          company: campaign.target_company
        },
        payload_link: 'https://malicious.example.com/payload',
        template_type: campaign.template_type
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setEmail(response.data);
    } catch (error) {
      console.error('Error crafting email:', error);
    }
    setLoading(false);
  };

  const createCampaign = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(`${API_URL}/social/campaign`, campaign, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert('Campaign created successfully!');
    } catch (error) {
      console.error('Error creating campaign:', error);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-900 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center gap-3 mb-6">
          <Target className="w-8 h-8 text-red-400" />
          <h1 className="text-3xl font-bold text-white">Social Engineering</h1>
        </div>

        {/* Warning Banner */}
        <div className="bg-red-900/20 border border-red-500 rounded-lg p-4 mb-6 flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
          <div className="text-sm text-red-300">
            <p className="font-bold mb-1">AUTHORIZATION REQUIRED</p>
            <p>Only use on targets you have explicit written permission to test. Unauthorized use is illegal.</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* OSINT Collection */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <Search className="w-5 h-5" />
              OSINT Collection
            </h2>

            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-2">Target</label>
                <input
                  type="text"
                  value={target}
                  onChange={(e) => setTarget(e.target.value)}
                  className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg"
                  placeholder="example.com or john.doe@example.com"
                />
              </div>

              <div>
                <label className="block text-sm text-gray-400 mb-2">Target Type</label>
                <select
                  value={targetType}
                  onChange={(e) => setTargetType(e.target.value)}
                  className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg"
                >
                  <option value="domain">Domain</option>
                  <option value="email">Email</option>
                  <option value="name">Name</option>
                  <option value="ip">IP Address</option>
                </select>
              </div>

              <button
                onClick={gatherOSINT}
                disabled={loading}
                className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
              >
                {loading ? 'Gathering...' : 'Gather OSINT'}
              </button>

              {osintResults && (
                <div className="mt-4 p-4 bg-gray-700 rounded-lg">
                  <h3 className="text-white font-bold mb-2">Results:</h3>
                  <pre className="text-xs text-gray-300 overflow-auto max-h-64">
                    {JSON.stringify(osintResults, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          </div>

          {/* Email Crafting */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <Mail className="w-5 h-5" />
              Email Crafting
            </h2>

            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-2">Template Type</label>
                <select
                  value={campaign.template_type}
                  onChange={(e) => setCampaign({ ...campaign, template_type: e.target.value })}
                  className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg"
                >
                  <option value="urgent_security">Urgent Security Alert</option>
                  <option value="invoice">Invoice Payment</option>
                  <option value="password_reset">Password Reset</option>
                  <option value="job_offer">Job Opportunity</option>
                </select>
              </div>

              <div>
                <label className="block text-sm text-gray-400 mb-2">Target Name</label>
                <input
                  type="text"
                  value={campaign.target_name}
                  onChange={(e) => setCampaign({ ...campaign, target_name: e.target.value })}
                  className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg"
                  placeholder="John Doe"
                />
              </div>

              <div>
                <label className="block text-sm text-gray-400 mb-2">Company</label>
                <input
                  type="text"
                  value={campaign.target_company}
                  onChange={(e) => setCampaign({ ...campaign, target_company: e.target.value })}
                  className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg"
                  placeholder="Tech Corp"
                />
              </div>

              <button
                onClick={craftEmail}
                disabled={loading}
                className="w-full px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50"
              >
                Generate Email
              </button>

              {email && (
                <div className="mt-4 p-4 bg-gray-700 rounded-lg space-y-2">
                  <div>
                    <span className="text-gray-400 text-sm">Subject:</span>
                    <p className="text-white">{email.subject}</p>
                  </div>
                  <div>
                    <span className="text-gray-400 text-sm">Body:</span>
                    <pre className="text-white text-sm whitespace-pre-wrap mt-1">{email.body}</pre>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Campaign Creation */}
        <div className="mt-6 bg-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <Send className="w-5 h-5" />
            Create Campaign
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-gray-400 mb-2">Campaign Name</label>
              <input
                type="text"
                value={campaign.name}
                onChange={(e) => setCampaign({ ...campaign, name: e.target.value })}
                className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg"
                placeholder="Q1 Security Test"
              />
            </div>

            <div>
              <label className="block text-sm text-gray-400 mb-2">Target Email</label>
              <input
                type="email"
                value={campaign.target_email}
                onChange={(e) => setCampaign({ ...campaign, target_email: e.target.value })}
                className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg"
                placeholder="target@example.com"
              />
            </div>
          </div>

          <button
            onClick={createCampaign}
            disabled={loading}
            className="mt-4 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
          >
            Create Campaign
          </button>
        </div>
      </div>
    </div>
  );
}
