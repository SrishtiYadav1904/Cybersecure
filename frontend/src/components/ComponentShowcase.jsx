import React, { useState } from 'react';
import {
  Sparkles,
  ShieldCheck,
  AlertTriangle,
  HeartHandshake,
  Search,
  User,
  Plus,
  Send,
  Download,
  Info
} from 'lucide-react';
import Button from './ui/Button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from './ui/Card';
import Badge from './ui/Badge';
import Input from './ui/Input';
import Select from './ui/Select';
import Tabs from './ui/Tabs';
import Modal from './ui/Modal';
import Drawer from './ui/Drawer';
import Skeleton from './ui/Skeleton';
import EmptyState from './ui/EmptyState';
import Toast from './ui/Toast';
import Tooltip from './ui/Tooltip';

export default function ComponentShowcase() {
  const [modalOpen, setModalOpen] = useState(false);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('one');

  return (
    <div className="space-y-10 max-w-5xl mx-auto py-4 animate-fade-in">
      <div>
        <h2 className="text-2xl font-bold text-white tracking-tight">
          CyberGuard UI Design System Showcase
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Visual inventory of design tokens, variants, interactive states, and reusable atoms.
        </p>
      </div>

      {/* 1. Buttons */}
      <Card className="p-6 space-y-4">
        <CardTitle>Button Variants & States</CardTitle>
        <div className="flex flex-wrap items-center gap-3">
          <Button variant="primary" icon={Sparkles}>Primary Button</Button>
          <Button variant="secondary" icon={Search}>Secondary</Button>
          <Button variant="danger" icon={AlertTriangle}>Danger / Action</Button>
          <Button variant="ghost">Ghost Button</Button>
          <Button variant="outline">Outline</Button>
          <Button variant="primary" isLoading>Loading</Button>
          <Button variant="primary" disabled>Disabled</Button>
        </div>
        <div className="flex flex-wrap items-center gap-3 pt-2">
          <Button variant="primary" size="sm">Small (sm)</Button>
          <Button variant="primary" size="md">Medium (md)</Button>
          <Button variant="primary" size="lg">Large (lg)</Button>
        </div>
      </Card>

      {/* 2. Badges */}
      <Card className="p-6 space-y-4">
        <CardTitle>Badges & Severity Variants</CardTitle>
        <div className="flex flex-wrap items-center gap-3">
          <Badge variant="safe">SAFE / CLEAN</Badge>
          <Badge variant="concerning">CONCERNING / MODERATE</Badge>
          <Badge variant="harmful">HARMFUL / HIGH</Badge>
          <Badge variant="severe">SEVERE / CRITICAL</Badge>
          <Badge variant="info">INFO / TELEMETRY</Badge>
          <Badge variant="default">DEFAULT / STANDBY</Badge>
          <Badge variant="outline">OUTLINE</Badge>
        </div>
      </Card>

      {/* 3. Inputs & Selects */}
      <Card className="p-6 space-y-4">
        <CardTitle>Form Elements (Inputs & Selects)</CardTitle>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label="Standard Input"
            placeholder="Type your message..."
            helperText="Clear helper text describing required input."
            icon={User}
          />
          <Input
            label="Input with Error State"
            placeholder="Invalid text..."
            error="This field is required and cannot be empty."
            defaultValue="Invalid content"
          />
          <Select
            label="Platform Selection"
            options={[
              { value: 'Instagram', label: 'Instagram' },
              { value: 'WhatsApp', label: 'WhatsApp' },
              { value: 'Twitter', label: 'X / Twitter' }
            ]}
          />
        </div>
      </Card>

      {/* 4. Tabs & Segmented Controls */}
      <Card className="p-6 space-y-4">
        <CardTitle>Tabs & Segmented Controls</CardTitle>
        <div className="space-y-4">
          <Tabs
            tabs={[
              { id: 'one', label: 'First Tab' },
              { id: 'two', label: 'Second Tab', badge: '3' },
              { id: 'three', label: 'Third Tab' }
            ]}
            activeTab={activeTab}
            onChange={setActiveTab}
            variant="segmented"
          />

          <Tabs
            tabs={[
              { id: 'one', label: 'Underline View' },
              { id: 'two', label: 'Timeline Events' },
              { id: 'three', label: 'Model Evaluation' }
            ]}
            activeTab={activeTab}
            onChange={setActiveTab}
            variant="underline"
          />
        </div>
      </Card>

      {/* 5. Modals & Drawers */}
      <Card className="p-6 space-y-4">
        <CardTitle>Overlay Systems (Modals & Drawers)</CardTitle>
        <div className="flex gap-3">
          <Button variant="secondary" onClick={() => setModalOpen(true)}>
            Open Test Modal
          </Button>
          <Button variant="secondary" onClick={() => setDrawerOpen(true)}>
            Open Test Drawer
          </Button>
        </div>
      </Card>

      {/* 6. Alerts & Toasts */}
      <Card className="p-6 space-y-4">
        <CardTitle>Notification Toasts & Alerts</CardTitle>
        <div className="space-y-2.5">
          <Toast type="success" message="Analysis saved successfully to incident record." />
          <Toast type="error" message="Unable to connect to OCR microservice. Check network." />
          <Toast type="warning" message="Model Population Stability Index indicates slight drift." />
          <Toast type="info" message="Production model CB-EXP-002 active and serving live inference." />
        </div>
      </Card>

      {/* 7. Skeletons */}
      <Card className="p-6 space-y-4">
        <CardTitle>Loading Skeletons</CardTitle>
        <Skeleton variant="text" count={2} />
        <Skeleton variant="card" />
      </Card>

      {/* 8. Empty State */}
      <Card className="p-6 space-y-4">
        <CardTitle>Empty State Component</CardTitle>
        <EmptyState
          icon={ShieldCheck}
          title="No Items Found"
          description="Everything is in order. Start an action to generate data."
          actionLabel="Primary Action"
          onAction={() => alert('Empty state clicked')}
        />
      </Card>

      {/* Modal Demo */}
      <Modal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        title="Interactive Modal Example"
        description="Accessible modal container with escape listener and backdrop dismiss."
        footer={
          <Button variant="primary" size="sm" onClick={() => setModalOpen(false)}>
            Close Modal
          </Button>
        }
      >
        <p className="text-xs text-slate-300">
          Modal content is cleanly padded with full keyboard accessibility.
        </p>
      </Modal>

      {/* Drawer Demo */}
      <Drawer
        isOpen={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        title="Slide-over Drawer Panel"
        footer={
          <Button variant="secondary" size="sm" onClick={() => setDrawerOpen(false)}>
            Close Drawer
          </Button>
        }
      >
        <p className="text-xs text-slate-300">
          Drawers provide non-intrusive side sheets for secondary navigation, filters, or audit histories.
        </p>
      </Drawer>
    </div>
  );
}
