package de.catgirlwolf.client;

import com.mojang.blaze3d.vertex.PoseStack;
import de.catgirlwolf.CatgirlWolf;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.client.renderer.entity.state.WolfRenderState;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.animal.wolf.Wolf;

/**
 * Zeichnet den Vanilla-Wolf mit dem Catgirl-Modell.
 * Modell-Einheiten entsprechen dem Spielermodell; 0,9375 ist dieselbe Skalierung,
 * die Minecraft für Spieler verwendet (ca. 1,8 Blöcke hoch, Ohren etwas darüber).
 */
public class CatgirlWolfRenderer extends MobRenderer<Wolf, WolfRenderState, CatgirlWolfModel> {
	public static final Identifier TEXTURE =
			Identifier.fromNamespaceAndPath(CatgirlWolf.MOD_ID, "textures/entity/catgirl_wolf.png");
	private static final float PLAYER_SCALE = 0.9375F;

	public CatgirlWolfRenderer(EntityRendererProvider.Context context) {
		super(context, new CatgirlWolfModel(context.bakeLayer(CatgirlWolfModel.LAYER)), 0.45F);
	}

	@Override
	public WolfRenderState createRenderState() {
		return new WolfRenderState();
	}

	@Override
	public void extractRenderState(Wolf wolf, WolfRenderState state, float partialTick) {
		super.extractRenderState(wolf, state, partialTick);
		state.isAngry = wolf.isAngry();
		state.isSitting = wolf.isInSittingPose();
		state.tailAngle = wolf.getTailAngle();
		state.headRollAngle = wolf.getHeadRollAngle(partialTick);
		state.shakeAnim = wolf.getShakeAnim(partialTick);
		state.wetShade = wolf.getWetShade(partialTick);
	}

	@Override
	public Identifier getTextureLocation(WolfRenderState state) {
		return TEXTURE;
	}

	@Override
	protected void scale(WolfRenderState state, PoseStack poseStack) {
		float s = PLAYER_SCALE * (state.isBaby ? 0.5F : 1.0F);
		poseStack.scale(s, s, s);
	}
}
