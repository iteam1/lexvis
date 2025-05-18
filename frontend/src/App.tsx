import React, { useState, lazy, Suspense } from 'react';
import { Upload, Button, Card, Row, Col, Input, message, Tabs, Typography, Spin } from 'antd';
import { UploadOutlined, CodeOutlined, FileTextOutlined } from '@ant-design/icons';
import axios from 'axios';
import 'antd/dist/antd.min.css';
import './App.css';

// Lazy load ReactJson to avoid SSR issues
const ReactJson = lazy(() => import('react-json-view'));

const { TextArea } = Input;
const { TabPane } = Tabs;
const { Title, Text } = Typography;

interface TokenInfo {
  text: string;
  type: string;
  line: number;
  column: number;
  channel: number;
  token_index: number;
  start: number;
  stop: number;
}

const App: React.FC = () => {
  const [grammarFile, setGrammarFile] = useState<File | null>(null);
  const [inputText, setInputText] = useState('');
  const [tokens, setTokens] = useState<TokenInfo[]>([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('1');

  const handleGrammarUpload = (file: File) => {
    setGrammarFile(file);
    return false; // Prevent auto upload
  };

  const tokenizeInput = async () => {
    if (!grammarFile) {
      message.error('Please upload a grammar file first');
      return;
    }

    if (!inputText.trim()) {
      message.error('Please enter some text to tokenize');
      return;
    }

    setLoading(true);
    
    const formData = new FormData();
    formData.append('grammar_file', grammarFile);
    formData.append('input_text', inputText);

    try {
      // In development, use the proxy defined in package.json
      const response = await axios.post('/api/tokenize', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      setTokens(response.data.tokens);
      message.success('Text tokenized successfully!');
      setActiveTab('2');
    } catch (error) {
      console.error('Error tokenizing input:', error);
      message.error('Failed to tokenize input. Please check the console for details.');
    } finally {
      setLoading(false);
    }
  };

  const renderToken = (token: TokenInfo, index: number) => {
    return (
      <div 
        key={index} 
        className="token" 
        style={{
          display: 'inline-block',
          margin: '2px',
          padding: '2px 6px',
          borderRadius: '4px',
          backgroundColor: '#f0f2f5',
          border: '1px solid #d9d9d9',
        }}
        title={`Type: ${token.type}\nLine: ${token.line}, Column: ${token.column}`}
      >
        <Text strong>{token.text}</Text>
        <div style={{ fontSize: '0.8em', color: '#666' }}>{token.type}</div>
      </div>
    );
  };

  return (
    <div className="App">
      <div style={{ padding: '24px' }}>
        <Title level={2} style={{ textAlign: 'center', marginBottom: '24px' }}>
          ANTLR Token Visualizer
        </Title>
        
        <Row gutter={[16, 16]}>
          <Col xs={24} md={12}>
            <Card 
              title={
                <>
                  <FileTextOutlined /> Grammar File
                </>
              }
              style={{ height: '100%' }}
            >
              <Upload.Dragger
                name="grammar"
                multiple={false}
                beforeUpload={handleGrammarUpload}
                fileList={grammarFile ? [{
                  uid: '1',
                  name: grammarFile.name,
                  size: grammarFile.size,
                  type: grammarFile.type,
                }] : []}
                onRemove={() => {
                  setGrammarFile(null);
                  return false;
                }}
              >
                <p className="ant-upload-drag-icon">
                  <UploadOutlined />
                </p>
                <p className="ant-upload-text">
                  Click or drag grammar file to this area
                </p>
                <p className="ant-upload-hint">
                  Supports .g4 ANTLR grammar files
                </p>
              </Upload.Dragger>
            </Card>
          </Col>
          
          <Col xs={24} md={12}>
            <Card 
              title={
                <>
                  <CodeOutlined /> Input Text
                </>
              }
              style={{ height: '100%' }}
              actions={[
                <Button 
                  key="tokenize" 
                  type="primary" 
                  onClick={tokenizeInput}
                  loading={loading}
                  disabled={!grammarFile || !inputText.trim()}
                >
                  Tokenize
                </Button>
              ]}
            >
              <TextArea
                rows={8}
                placeholder="Enter text to tokenize..."
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                style={{ width: '100%' }}
              />
            </Card>
          </Col>
        </Row>

        {tokens.length > 0 && (
          <Card 
            title="Tokenization Results" 
            style={{ marginTop: '24px' }}
          >
            <Tabs 
              activeKey={activeTab} 
              onChange={setActiveTab}
            >
              <TabPane tab="Visual" key="1">
                <div style={{ 
                  minHeight: '200px', 
                  padding: '16px', 
                  border: '1px solid #f0f0f0', 
                  borderRadius: '4px',
                  whiteSpace: 'pre-wrap',
                  fontFamily: 'monospace',
                  backgroundColor: '#fafafa'
                }}>
                  {tokens.map((token, index) => renderToken(token, index))}
                </div>
              </TabPane>
              <TabPane tab="Raw Data" key="2">
                <div style={{ maxHeight: '500px', overflow: 'auto' }}>
                  <Suspense fallback={<div style={{ textAlign: 'center', padding: '20px' }}><Spin /></div>}>
                    <ReactJson 
                      src={tokens} 
                      name="tokens"
                      displayDataTypes={false}
                      collapsed={1}
                    />
                  </Suspense>
                </div>
              </TabPane>
            </Tabs>
          </Card>
        )}
      </div>
    </div>
  );
};

export default App;
