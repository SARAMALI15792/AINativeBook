/**
 * Institution Branding Page
 *
 * Configure institution branding including logo, colors, and custom CSS.
 * Acceptance: Branding preview before save functionality.
 */

'use client';

import { useState } from 'react';
import { Eye, Save, Upload } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { BrandingForm } from '@/components/institution/BrandingForm';
import { BrandingPreview } from '@/components/institution/BrandingPreview';

export default function BrandingPage() {
  const [showPreview, setShowPreview] = useState(false);
  const [brandingData, setBrandingData] = useState({
    logoUrl: '',
    primaryColor: '#2e8555',
    secondaryColor: '#1a73e8',
    welcomeMessage: 'Welcome to our learning platform',
    customCss: '',
  });

  const handleSave = async () => {
    // TODO: Implement save to API
    console.log('Saving branding:', brandingData);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Branding</h1>
          <p className="text-muted-foreground mt-2">
            Customize your institution's appearance and messaging
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => setShowPreview(!showPreview)}>
            <Eye className="h-4 w-4 mr-2" />
            {showPreview ? 'Hide' : 'Show'} Preview
          </Button>
          <Button onClick={handleSave}>
            <Save className="h-4 w-4 mr-2" />
            Save Changes
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Branding Form */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Logo</CardTitle>
              <CardDescription>
                Upload your institution's logo (recommended: 200x60px PNG)
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center gap-4">
                <div className="w-48 h-16 bg-gray-100 rounded-lg flex items-center justify-center border-2 border-dashed">
                  {brandingData.logoUrl ? (
                    <img
                      src={brandingData.logoUrl}
                      alt="Logo preview"
                      className="max-w-full max-h-full object-contain"
                    />
                  ) : (
                    <span className="text-sm text-muted-foreground">
                      No logo uploaded
                    </span>
                  )}
                </div>
                <Button variant="outline" size="sm">
                  <Upload className="h-4 w-4 mr-2" />
                  Upload Logo
                </Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Colors</CardTitle>
              <CardDescription>
                Choose colors that match your brand identity
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="primaryColor">Primary Color</Label>
                <div className="flex items-center gap-4">
                  <Input
                    id="primaryColor"
                    type="color"
                    value={brandingData.primaryColor}
                    onChange={(e) =>
                      setBrandingData({ ...brandingData, primaryColor: e.target.value })
                    }
                    className="w-20 h-10"
                  />
                  <Input
                    type="text"
                    value={brandingData.primaryColor}
                    onChange={(e) =>
                      setBrandingData({ ...brandingData, primaryColor: e.target.value })
                    }
                    className="flex-1 font-mono"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="secondaryColor">Secondary Color</Label>
                <div className="flex items-center gap-4">
                  <Input
                    id="secondaryColor"
                    type="color"
                    value={brandingData.secondaryColor}
                    onChange={(e) =>
                      setBrandingData({ ...brandingData, secondaryColor: e.target.value })
                    }
                    className="w-20 h-10"
                  />
                  <Input
                    type="text"
                    value={brandingData.secondaryColor}
                    onChange={(e) =>
                      setBrandingData({ ...brandingData, secondaryColor: e.target.value })
                    }
                    className="flex-1 font-mono"
                  />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Welcome Message</CardTitle>
              <CardDescription>
                Message shown to students when they log in
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Textarea
                value={brandingData.welcomeMessage}
                onChange={(e) =>
                  setBrandingData({ ...brandingData, welcomeMessage: e.target.value })
                }
                placeholder="Enter a welcome message..."
                rows={4}
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Custom CSS</CardTitle>
              <CardDescription>
                Advanced: Add custom CSS for additional styling
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Textarea
                value={brandingData.customCss}
                onChange={(e) =>
                  setBrandingData({ ...brandingData, customCss: e.target.value })
                }
                placeholder=".custom-class { color: #333; }"
                rows={8}
                className="font-mono text-sm"
              />
            </CardContent>
          </Card>
        </div>

        {/* Preview */}
        {showPreview && (
          <div className="lg:sticky lg:top-6 h-fit">
            <BrandingPreview brandingData={brandingData} />
          </div>
        )}
      </div>
    </div>
  );
}
