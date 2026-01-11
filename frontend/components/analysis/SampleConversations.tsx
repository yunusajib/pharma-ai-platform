'use client';

import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useState } from 'react';

interface SampleConversationsProps {
  onLoadSample: (conversation: string) => void;
}

const SAMPLE_CONVERSATIONS = [
  {
    title: '✅ Excellent Performance (Score: ~4.5)',
    description: 'Great objection handling, strong relationship building',
    conversation: `Rep: Good morning Dr. Martinez! Thanks for taking the time to meet with me today. How have your patients been responding to their current cholesterol treatments?

Dr: Morning. They're doing okay, but I'm seeing some adherence issues with the generic statins. The side effects are a concern for some patients.

Rep: I completely understand - adherence is such a critical factor in long-term outcomes. That's actually one of the key differentiators I wanted to discuss with CardioStatin. Our clinical data shows a 40% reduction in muscle-related side effects compared to older statins, which directly translates to better adherence rates.

Dr: That's interesting, but I have to be honest - the cost is significantly higher than the generics. It's hard to justify that to patients, especially those on fixed incomes.

Rep: That's a very valid concern, and I appreciate you advocating for your patients' financial wellbeing. What many physicians find is that when we look at total cost of care, CardioStatin actually becomes more cost-effective. The improved adherence means fewer cardiovascular events - we're seeing 30% fewer ER visits and hospitalizations in our real-world evidence studies. For a patient on Medicare, that potential $50,000 hospitalization cost far outweighs the annual difference in medication cost.

Dr: That makes sense when you frame it that way. Do you have data specific to elderly patients? Most of my hyperlipidemia patients are 65+.

Rep: Absolutely - and that's actually where CardioStatin shines. In our subgroup analysis of patients over 65, we saw a 35% reduction in major adverse cardiac events compared to standard therapy. I'd love to send you the full study data, and we also have a patient assistance program that can help with out-of-pocket costs for those who qualify.

Dr: Okay, send me that data. I'd like to review it before making any changes to my prescribing.

Rep: Perfect. I'll email you the clinical data and outcomes analysis by tomorrow morning. Would it be helpful if I followed up with you next Thursday at 2pm to discuss any questions you might have after reviewing the materials? I can schedule 15 minutes on your calendar.

Dr: Thursday at 2 works. Send me a calendar invite.

Rep: Will do. Thank you so much for your time today, Dr. Martinez. I really appreciate your thoughtful approach to patient care.`,
  },
  {
    title: '⚠️ Needs Improvement (Score: ~3.2)',
    description: 'Poor objection handling, vague follow-up',
    conversation: `Rep: Hey Dr. Smith, got a minute to talk about CardioStatin?

Dr: I'm pretty busy, but sure, make it quick.

Rep: So CardioStatin is our newest cholesterol drug and it's way better than what you're probably using now.

Dr: I'm happy with what I'm currently prescribing. The generics work fine.

Rep: Yeah but this is newer and has better outcomes.

Dr: How much better? And what's the cost?

Rep: Um, I'd have to look up the exact numbers, but it's definitely better. The cost is competitive.

Dr: Competitive with what? Generic atorvastatin costs pennies.

Rep: Well, quality costs more. You get what you pay for.

Dr: I need real data, not sales pitches. Do you have any studies?

Rep: Yeah we have tons of studies. I can send them to you.

Dr: Okay, send them and we can talk later maybe.

Rep: Sounds good! I'll be in touch.

Dr: Alright, I need to go.`,
  },
  {
    title: '🔴 Critical Issues (Score: ~2.1)',
    description: 'Compliance violations, unprofessional tone',
    conversation: `Rep: Hey doc, you need to start prescribing CardioStatin instead of those cheap generics.

Dr: Excuse me? I prescribe based on evidence and what's best for my patients.

Rep: Look, I know the generics are cheaper but CardioStatin is better for everything. We're even seeing it help with migraines in some patients.

Dr: Migraines? That's not an approved indication. What are you talking about?

Rep: Yeah, off-label use. Lots of docs are using it for headache prevention and seeing great results.

Dr: That's completely inappropriate. I'm not interested in off-label promotion.

Rep: Come on, everyone does off-label. Don't be so uptight about it.

Dr: I think we're done here.

Rep: Wait, just try it with a few patients. I'll even give you some samples.

Dr: Please leave. I'm not interested.`,
  },
];

export default function SampleConversations({ onLoadSample }: SampleConversationsProps) {
  const [expanded, setExpanded] = useState<number | null>(null);

  return (
    <Card className="p-6 mb-6 bg-white shadow-lg">
      <h3 className="text-lg font-bold text-gray-900 mb-3">
        📚 Sample Conversations (Try These!)
      </h3>
      <div className="space-y-3">
        {SAMPLE_CONVERSATIONS.map((sample, idx) => (
          <div key={idx} className="border border-gray-200 rounded-lg overflow-hidden">
            <div
              className="p-3 bg-gray-50 cursor-pointer hover:bg-gray-100 transition-colors flex items-center justify-between"
              onClick={() => setExpanded(expanded === idx ? null : idx)}
            >
              <div>
                <div className="font-semibold text-gray-900">{sample.title}</div>
                <div className="text-sm text-gray-600">{sample.description}</div>
              </div>
              <span className="text-gray-400">
                {expanded === idx ? '▼' : '▶'}
              </span>
            </div>

            {expanded === idx && (
              <div className="p-4 bg-white border-t border-gray-200">
                <div className="text-sm text-gray-700 font-mono bg-gray-50 p-3 rounded mb-3 max-h-48 overflow-y-auto">
                  {sample.conversation}
                </div>
                <Button
                  onClick={() => onLoadSample(sample.conversation)}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white"
                >
                  Load This Conversation
                </Button>
              </div>
            )}
          </div>
        ))}
      </div>
    </Card>
  );
}
