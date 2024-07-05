-- /rl=reload
SLASH_RELOAD1 = "/rl"
SlashCmdList["RELOAD"] = function(args)
    ReloadUI()
end


-- 声明主表, 插件的内存对象
ColorFrame = {}
-- 创建配置面板
ColorFrame.panel = CreateFrame("Frame", "ColorFrame", UIParent)
ColorFrame.panel.name = "ColorFrame"

-- 添加到界面选项
InterfaceOptions_AddCategory(ColorFrame.panel)

-- 创建标题
local title = ColorFrame.panel:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
title:SetPoint("TOPLEFT", 16, -16)
title:SetText("ColorFrame")

-- 工具类
Util = {}

-- 创建checkbox公用方法
function Util.newCheckbox(label, description, onClick)
    local check = CreateFrame("CheckButton", "ColorFrame" .. label, ColorFrame.panel, "InterfaceOptionsCheckButtonTemplate")
    check:SetScript("OnClick", function(self)
        local tick = self:GetChecked()
        onClick(self, tick and true or false)
        --if tick then
        --    PlaySound(856) -- SOUNDKIT.IG_MAINMENU_OPTION_CHECKBOX_ON
        --else
        --    PlaySound(857) -- SOUNDKIT.IG_MAINMENU_OPTION_CHECKBOX_OFF
        --end
    end)
    check.label = _G[check:GetName() .. "Text"]
    check.label:SetText(label)
    check.tooltipText = label
    check.tooltipRequirement = description
    return check
end


-- 创建输入框的方法
function Util.newEditBox(label, onEnterPressed)
    local editBox = CreateFrame("EditBox", "ColorFrame" .. label, ColorFrame.panel, "InputBoxTemplate")
    editBox:SetSize(200, 30)
    -- 设置输入框的属性
    editBox:SetAutoFocus(false) -- 不自动获取焦点
    editBox:SetMaxLetters(15)  -- 最大字符数

    --设置输入框的回车事件
    editBox:SetScript("OnEnterPressed", function(self)
        onEnterPressed(self, self:GetText())
        self:ClearFocus()
    end)
    -- 设置输入框的失去焦点事件
    editBox:SetScript("OnEscapePressed", function(self)
        self:ClearFocus()
    end)
    -- 设置输入框的失去焦点事件
    editBox:SetScript("OnShow", function(self)
        editBox:SetCursorPosition(0) -- 设置光标位置在文本开头
    end)
    -- 创建并设置标签
    local labelFrame = editBox:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    labelFrame:SetPoint("BOTTOMLEFT", editBox, "TOPLEFT", 0, 0)
    labelFrame:SetText(label)
    return editBox
end
