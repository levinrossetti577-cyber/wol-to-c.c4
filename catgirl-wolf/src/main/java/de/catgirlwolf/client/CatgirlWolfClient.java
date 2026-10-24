package de.catgirlwolf.client;

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.rendering.v1.ModelLayerRegistry;
import net.minecraft.client.renderer.entity.EntityRenderers;
import net.minecraft.world.entity.EntityType;

public class CatgirlWolfClient implements ClientModInitializer {
	@Override
	public void onInitializeClient() {
		ModelLayerRegistry.registerModelLayer(CatgirlWolfModel.LAYER, CatgirlWolfModel::createBodyLayer);
		// Ersetzt den Vanilla-Wolf-Renderer. Die Entity bleibt der echte Vanilla-Wolf.
		EntityRenderers.register(EntityType.WOLF, CatgirlWolfRenderer::new);
	}
}
